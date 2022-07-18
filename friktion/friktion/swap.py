#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
""" Module to call Swap contract """
import asyncio
import time
from enum import Enum
from typing import Tuple

import spl.token._layouts as layouts
from anchorpy import Provider, Wallet
from nacl import signing
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Processed
from solana.system_program import SYS_PROGRAM_ID
from solana.sysvar import SYSVAR_INSTRUCTIONS_PUBKEY, SYSVAR_RENT_PUBKEY
from solana.transaction import Transaction
from solana.utils.helpers import decode_byte_string
from spl.token.async_client import AsyncToken
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID

from friktion.friktion_anchor.instructions import cancel, claim
from friktion.inertia_anchor.accounts import OptionsContract
from friktion.offer import Offer
from friktion.pda import DELEGATE_AUTHORITY_ADDRESS, SwapOrderAddresses

from .bid_details import BidDetails
from .friktion_anchor.accounts import SwapOrder
from .friktion_anchor.instructions import create, exec, exec_msg
from .friktion_anchor.program_id import PROGRAM_ID
from .swap_order_template import SwapOrderTemplate

GLOBAL_FRIKTION_AUTHORITY = PublicKey("7wYqGsQmfVigMSratssoPddfLU1P5srZcM32nvKAgWkj")


def get_token_account(token_account_pk: PublicKey):
    http_client = Client(commitment=Processed)
    resp = http_client.get_account_info(token_account_pk)
    account_data = layouts.ACCOUNT_LAYOUT.parse(
        decode_byte_string(resp["result"]["value"]["data"][0])
    )
    return account_data


class Network(Enum):
    DEVNET = 1
    TESTNET = 2
    MAINNET = 3


def get_url_for_network(network: Network) -> str:
    if network == Network.DEVNET:
        return "https://api.devnet.solana.com"
    elif network == Network.TESTNET:
        return "https://api.testnet.solana.com"
    else:
        # mainnet
        return "https://solana-api.projectserum.com"


MIN_REQUIRED_ALLOWANCE = 100


# ---------------------------------------------------------------------------
# Swap Program
# ---------------------------------------------------------------------------
class SwapContract:

    network: Network
    url: str

    def __init__(self, network: Network):
        self.network = network
        self.url = get_url_for_network(network)

    # delegate should be the PDA of the swap order
    def give_allowance(
        self, wallet: Wallet, token_acct_to_delegate: PublicKey, mint: PublicKey, allowance: int
    ) -> bool:

        client = Client(self.url)
        token = Token(client, mint, TOKEN_PROGRAM_ID, wallet.payer)

        # acct_info = token.get_account_info(token_acct_to_delegate)
        # use a global authority for all swaps
        # assert acct_info.owner == swap_order.counterparty

        token.approve(
            token_acct_to_delegate, DELEGATE_AUTHORITY_ADDRESS, wallet.public_key, allowance
        )

        return True

    # delegate should be the PDA of the swap order
    def verify_allowance(self, mint: PublicKey, token_account: PublicKey) -> bool:
        client = Client(self.url)
        token = Token(client, mint, TOKEN_PROGRAM_ID, Keypair.generate())
        acct_info = token.get_account_info(token_account)
        return (
            acct_info.delegate == DELEGATE_AUTHORITY_ADDRESS
            and acct_info.delegated_amount >= MIN_REQUIRED_ALLOWANCE
        )

    def get_allowance_and_amount(
        self, mint: PublicKey, token_account: PublicKey
    ) -> Tuple[int, int]:
        client = Client(self.url)
        token = Token(client, mint, TOKEN_PROGRAM_ID, Keypair.generate())
        acct_info = token.get_account_info(token_account)
        return acct_info.delegated_amount, acct_info.amount

    async def get_offered_token_details(self, swap_order_addr: PublicKey):
        swap_order = await self.get_swap_order(swap_order_addr)
        options_contract = await self.get_options_contract_for_key(swap_order.options_contract)
        ul_factor = await self._get_token_norm_factor(options_contract.underlying_mint)
        quote_factor = await self._get_token_norm_factor(options_contract.quote_mint)
        strike_price = (
            (ul_factor / quote_factor)
            * options_contract.quote_amount
            / options_contract.underlying_amount
            if options_contract.is_call
            else (quote_factor / ul_factor)
            * options_contract.underlying_amount
            / options_contract.quote_amount
        )
        return {
            'underlyingAsset': options_contract.underlying_mint,
            'expiryTimestamp': options_contract.expiry_ts,
            'isPut': not options_contract.is_call,
            'strikeAsset': options_contract.quote_mint,
            'strikePrice': strike_price,
            'collateralAsset': options_contract.underlying_mint,
        }

    async def _get_token_norm_factor(self, mint: PublicKey) -> int:
        client = AsyncClient(self.url)
        await client.is_connected()

        give_token = AsyncToken(client, mint, TOKEN_PROGRAM_ID, Keypair.generate())

        return 10 ** (await give_token.get_mint_info()).decimals

    async def get_options_contract_for_key(self, key: PublicKey) -> OptionsContract:
        client = AsyncClient(self.url)
        await client.is_connected()

        acc = await OptionsContract.fetch(client, key)

        if acc is None:
            raise ValueError("No options contract found for key = ", key)

        await client.close()
        return acc

    async def get_swap_order(self, swap_order_addr: PublicKey) -> SwapOrder:
        client = AsyncClient(self.url)
        await client.is_connected()

        acc = await SwapOrder.fetch(client, swap_order_addr)

        if acc is None:
            raise ValueError(f"No swap order found for key = {swap_order_addr}")

        await client.close()
        return acc

    async def get_offer_details(self, swap_order_addr: PublicKey) -> Offer:
        swap_order = await self.get_swap_order(swap_order_addr)
        return Offer.from_swap_order(swap_order, swap_order_addr)

    async def validate_bid(self, swap_order_addr: PublicKey, bid_details: BidDetails) -> dict:
        offer: Offer = await self.get_offer_details(swap_order_addr)

        # TODO: evaluate adding expiry to the offer so it not necessary
        #       to call get_swap_order again
        swap_order: SwapOrder = await self.get_swap_order(swap_order_addr)

        if bid_details.bid_size < offer.minBidSize:
            return {"error": "bid size is below min bid size"}
        if bid_details.bid_size > offer.offerAmount:
            return {"error": "bid size is greater than offer size"}
        if bid_details.bid_price < offer.minPrice:
            return {"error": "bid price is less than min price"}

        verified_allowance = self.verify_allowance(
            offer.biddingToken, bid_details.counterparty_receive_pool
        )
        if not verified_allowance:
            return {"error": "counterparty receive pool does not have sufficient allowance"}

        (allowance, amount) = self.get_allowance_and_amount(
            offer.biddingToken, bid_details.counterparty_receive_pool
        )

        transfer_amount = bid_details.bid_size * bid_details.bid_price
        if allowance < transfer_amount:
            return {"error": "allowance is below required threshold"}

        if amount < transfer_amount:
            return {"error": "amount in token account is below required threshold"}

        # optional check for counterparty
        # if swap_order.is_counterparty_provided and  != swap_order.counterparty:
        #     return {
        #         "error": "counterparty wallet pubkey doesn't match given swap order"
        #     }
        if swap_order.expiry < int(time.time()):
            return {"error": "expiry was in the past"}
        # TODO: check mint of give pools and receive pools match
        # elif bid_details.counterparty_give_pool = swap_
        return {"error": None}

    async def create_offer(
        self, wallet: Wallet, template: SwapOrderTemplate
    ) -> Tuple[SwapOrder, PublicKey]:
        """
        Method to create offer
        Args:
            offer (dict): Offer dictionary containing necessary parameters
                to create a new offer
            wallet (Wallet): Wallet class instance
        Raises:
            TypeError: Offer argument is not a valid instance of Offer class
            ExecError: Transaction reverted
        Returns:
            offerId (int): OfferId of the created order
        """

        client = AsyncClient(self.url)
        await client.is_connected()

        pdas: SwapOrderAddresses = await SwapOrderAddresses.from_user(client, wallet.public_key)

        ix = create(
            {
                "give_size": template.give_size,
                "receive_size": template.receive_size,
                "expiry": template.expiry,
                "is_counterparty_provided": template.is_counterparty_provided,
                "is_whitelisted": template.is_whitelisted,
                "enforce_mint_match": False,
            },
            {
                "payer": wallet.public_key,  # signer
                "authority": wallet.public_key,
                "user_orders": pdas.user_orders_address,
                "swap_order": pdas.swap_order_address,
                "give_pool": pdas.give_pool_address,
                "give_mint": template.give_mint,
                "receive_pool": pdas.receive_pool_address,
                "receive_mint": template.receive_mint,
                "creator_give_pool": template.creator_give_pool,
                "counterparty": template.counterparty,
                "whitelist_token_mint": template.whitelist_token_mint,
                "options_contract": template.options_contract_key,
                "system_program": SYS_PROGRAM_ID,
                "token_program": TOKEN_PROGRAM_ID,
                "rent": SYSVAR_RENT_PUBKEY,
            },
        )

        tx = Transaction().add(ix)

        # print('create ix data: {}'.format(ix.data))
        # print('create ix accounts: {}'.format(ix.keys))

        provider = Provider(client, wallet)

        print('sending create tx...')
        tx_resp = await provider.send(tx, [])
        print(tx_resp)

        await client.confirm_transaction(tx_resp)

        await asyncio.sleep(1)
        acc = await self.get_swap_order(pdas.swap_order_address)

        await client.close()

        return (acc, pdas.swap_order_address)

    async def validate_and_exec_bid_msg(
        self,
        wallet: Wallet,
        bid_details: BidDetails,
        signed_msg: signing.SignedMessage,
    ):
        """
        Method to execute bid via signed message
        """

        client = AsyncClient(self.url)
        await client.is_connected()

        pdas = SwapOrderAddresses(bid_details.swap_order_owner, bid_details.order_id)
        swap_order = await self.get_swap_order(pdas.swap_order_address)

        error_dict = await self.validate_bid(pdas.swap_order_address, bid_details)
        if error_dict['error'] is not None:
            await client.close()
            return error_dict

        ix = exec_msg(
            {
                # "signature": str(signature.to_json()),
                "signature": str(signed_msg.signature),
                "caller": wallet.public_key,
                "raw_msg": str(signed_msg.message),
            },
            {
                "authority": wallet.public_key,  # signer
                "delegate_authority": pdas.delegate_authority_address,
                "swap_order": pdas.swap_order_address,
                "give_pool": swap_order.give_pool,
                "receive_pool": swap_order.receive_pool,
                "counterparty_give_pool": bid_details.counterparty_give_pool,
                "counterparty_receive_pool": bid_details.counterparty_receive_pool,
                # pass in a dummy value since not using whitelisting right now
                "whitelist_token_account": SYS_PROGRAM_ID,
                "instruction_sysvar": SYSVAR_INSTRUCTIONS_PUBKEY,
                "system_program": SYS_PROGRAM_ID,
                "token_program": TOKEN_PROGRAM_ID,
            },
        )

        tx = Transaction().add(ix)

        provider = Provider(client, wallet)

        print('sending exec MSG tx...')

        tx_resp = await provider.send(tx, [])

        print(tx_resp)

        await client.confirm_transaction(tx_resp)
        await client.close()

    async def validate_and_exec_bid(self, wallet: Wallet, bid_details: BidDetails):
        """
        Method to validate bid
        Args:
        Returns:
            response (dict): Dictionary containing number of errors (errors)
              and the corresponding error messages (messages)
        """

        client = AsyncClient(self.url)
        await client.is_connected()

        swap_order_owner = bid_details.swap_order_owner
        order_id = bid_details.order_id

        seeds = [
            str.encode("swapOrder"),
            bytes(swap_order_owner),
            order_id.to_bytes(8, byteorder="little"),
        ]
        [swap_order_addr, _] = PublicKey.find_program_address(seeds, PROGRAM_ID)
        swap_order = await self.get_swap_order(swap_order_addr)

        error_dict = await self.validate_bid(swap_order_addr, bid_details)
        if error_dict['error'] is not None:
            await client.close()
            return error_dict

        ix = exec(
            {
                "authority": wallet.public_key,  # signer
                "swap_order": swap_order_addr,
                "give_pool": swap_order.give_pool,
                "receive_pool": swap_order.receive_pool,
                "counterparty_give_pool": bid_details.counterparty_give_pool,
                "counterparty_receive_pool": bid_details.counterparty_receive_pool,
                # pass in a dummy value since not using whitelisting right now
                "whitelist_token_account": SYS_PROGRAM_ID,
                "system_program": SYS_PROGRAM_ID,
                "token_program": TOKEN_PROGRAM_ID,
            }
        )

        tx = Transaction().add(ix)

        provider = Provider(client, wallet)

        print('sending exec tx...')

        tx_resp = await provider.send(tx, [])

        print(tx_resp)

        await client.confirm_transaction(tx_resp)
        await client.close()

    async def reclaim_assets_post_fill(
        self,
        creator_wallet: Wallet,
        swap_order: PublicKey,
        give_pool: PublicKey,
        receive_pool: PublicKey,
    ) -> SwapOrder:
        """
        Method to create offer
        Args:
            offer (dict): Offer dictionary containing necessary parameters
                to create a new offer
            wallet (Wallet): Wallet class instance
        Raises:
            TypeError: Offer argument is not a valid instance of Offer class
            ExecError: Transaction reverted
        Returns:
            offerId (int): OfferId of the created order
        """

        client = AsyncClient(self.url)
        await client.is_connected()

        pdas: SwapOrderAddresses = SwapOrderAddresses(
            creator_wallet.public_key, swap_order_address=swap_order
        )
        ix = claim(
            {
                "authority": creator_wallet.public_key,
                "swap_order": pdas.swap_order_address,
                "give_pool": pdas.give_pool_address,
                "receive_pool": pdas.receive_pool_address,
                "creator_give_pool": give_pool,
                "creator_receive_pool": receive_pool,
                "system_program": SYS_PROGRAM_ID,
                "token_program": TOKEN_PROGRAM_ID,
            }
        )

        tx = Transaction().add(ix)

        provider = Provider(client, creator_wallet)

        print('sending claim tx...')
        tx_resp = await provider.send(tx, [])
        print(tx_resp)

        await client.confirm_transaction(tx_resp)

        await asyncio.sleep(1)
        acc = await self.get_swap_order(pdas.swap_order_address)

        await client.close()

        return acc

    async def cancel_order(self, wallet: Wallet, order_id: int, creator_give_pool: PublicKey):

        client = AsyncClient(self.url)
        await client.is_connected()

        pdas: SwapOrderAddresses = await SwapOrderAddresses.from_user(
            client, wallet.public_key, order_id=order_id
        )

        ix = cancel(
            {
                "authority": wallet.public_key,
                "swap_order": pdas.swap_order_address,
                "give_pool": pdas.give_pool_address,
                "creator_give_pool": creator_give_pool,
                "receive_pool": pdas.receive_pool_address,
                "system_program": SYS_PROGRAM_ID,
                "token_program": TOKEN_PROGRAM_ID,
            }
        )

        tx = Transaction().add(ix)

        provider = Provider(client, wallet)

        print('sending cancel tx...')
        tx_resp = await provider.send(tx, [])
        print(tx_resp)

        await client.confirm_transaction(tx_resp)
        await client.close()
