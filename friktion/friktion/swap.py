#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
""" Module to call Swap contract """
import asyncio
import time
from decimal import Decimal
from enum import Enum
from typing import Optional, Tuple

import spl.token._layouts as layouts
from anchorpy import Provider, Wallet
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Processed
from solana.system_program import SYS_PROGRAM_ID
from solana.sysvar import SYSVAR_INSTRUCTIONS_PUBKEY, SYSVAR_RENT_PUBKEY
from solana.transaction import Transaction
from solana.utils.helpers import decode_byte_string
from solders.signature import Signature
from spl.token.async_client import AsyncToken
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.core import AccountInfo
from spl.token.instructions import get_associated_token_address

from friktion.friktion_anchor.instructions import cancel, claim
from friktion.inertia_anchor.accounts import OptionsContract
from friktion.offer import Offer
from friktion.pda import DELEGATE_AUTHORITY_ADDRESS, SwapOrderAddresses, find_swap_order_address
from sdk_commons.config import OfferTokenDetails

from .bid_details import BidDetails
from .friktion_anchor.accounts import SwapOrder
from .friktion_anchor.instructions import create, exec, exec_msg
from .swap_order_template import SwapOrderTemplate

GLOBAL_FRIKTION_AUTHORITY = PublicKey("7wYqGsQmfVigMSratssoPddfLU1P5srZcM32nvKAgWkj")
GLOBAL_FRIKTION_ADMIN = PublicKey("DxMJgeSVoe1cWo1NPExiAsmn83N3bADvkT86dSP1k7WE")


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

# mainnet auction bid token
MAINNET_USDC_MINT = PublicKey("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")


# ----------------------------------------------------------------------
# Swap Program
# ----------------------------------------------------------------------
class SwapContract:

    network: Network
    url: str

    def __init__(self, network: Network):
        self.network = network
        self.url = get_url_for_network(network)

    # delegate should be the PDA of the swap order
    def give_allowance(self, wallet: Wallet, mint: PublicKey, allowance: int):
        client = Client(self.url)
        token = Token(client, mint, TOKEN_PROGRAM_ID, wallet.payer)

        # acct_info = token.get_account_info(token_acct_to_delegate)
        # use a global authority for all swaps
        # assert acct_info.owner == swap_order.counterparty

        token_acct_to_delegate = get_associated_token_address(wallet.public_key, mint)
        token.approve(
            token_acct_to_delegate, DELEGATE_AUTHORITY_ADDRESS, wallet.public_key, allowance
        )

    def get_account_info(self, mint: PublicKey, wallet_addr: PublicKey) -> AccountInfo:
        client = Client(self.url)
        token = Token(client, mint, TOKEN_PROGRAM_ID, Keypair.generate())
        receive_pool = get_associated_token_address(wallet_addr, mint)
        return token.get_account_info(receive_pool)

    def _has_minimum_allowance(self, account_info: AccountInfo) -> bool:
        return (
            account_info.delegate == DELEGATE_AUTHORITY_ADDRESS
            and account_info.delegated_amount >= MIN_REQUIRED_ALLOWANCE
        )

    # delegate should be the PDA of the swap order
    def verify_allowance(self, mint: PublicKey, wallet_addr: PublicKey) -> bool:
        acct_info = self.get_account_info(mint, wallet_addr)
        return self._has_minimum_allowance(acct_info)

    def get_allowance_and_amount(self, mint: PublicKey, wallet: PublicKey) -> Tuple[int, int]:
        acct_info = self.get_account_info(mint, wallet)
        return acct_info.delegated_amount, acct_info.amount

    async def get_offered_token_details(self, user: PublicKey, order_id: int) -> OfferTokenDetails:
        swap_order = await self.get_swap_order(user, order_id)
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
            'underlyingAsset': str(options_contract.underlying_mint),
            # options expiration is in seconds since epoch
            'expiryTimestamp': options_contract.expiry_ts,
            'isPut': not options_contract.is_call,
            'strikeAsset': str(options_contract.quote_mint),
            # float -> str -> Decimal to prevent changing
            # the precision due to floating point arithmetic
            'strikePrice': Decimal(str(strike_price)),
            'collateralAsset': str(options_contract.underlying_mint),
        }

    async def _get_token_norm_factor(self, mint: PublicKey) -> int:
        client = AsyncClient(self.url)
        await client.is_connected()

        give_token = AsyncToken(client, mint, TOKEN_PROGRAM_ID, Keypair.generate())

        # get_mint_info is untyped
        return 10 ** (await give_token.get_mint_info()).decimals  # type: ignore

    async def get_options_contract_for_key(self, key: PublicKey) -> OptionsContract:
        client = AsyncClient(self.url)
        await client.is_connected()

        acc = await OptionsContract.fetch(client, key)

        if acc is None:
            raise ValueError("No options contract found for key = ", key)

        await client.close()
        return acc

    async def get_swap_order_for_key(self, key: PublicKey) -> SwapOrder:
        client = AsyncClient(self.url)
        await client.is_connected()

        acc = await SwapOrder.fetch(client, key)

        if acc is None:
            raise ValueError("No swap order found for key = ", key)

        await client.close()
        return acc

    async def get_swap_order(self, user: PublicKey, order_id: int) -> SwapOrder:
        [addr, bump] = find_swap_order_address(user, order_id)
        return await self.get_swap_order_for_key(addr)

    async def get_offer_details(self, user: PublicKey, order_id: int) -> Offer:
        """
        Method to get offer details
        Args:
            offer_id (int): Offer ID
        Raises:
            ValueError: The argument is not a valid offer
        Returns:
            details (SwapOrder): Offer details
        """
        [addr, bump] = find_swap_order_address(user, order_id)
        swap_order = await self.get_swap_order_for_key(addr)
        return Offer.from_swap_order(swap_order, addr)

    async def _validate_bid_allowance(
        self, bidding_token: PublicKey, bid_details: BidDetails
    ) -> Optional[str]:
        acct_info = self.get_account_info(bidding_token, bid_details.signer_wallet)

        if not self._has_minimum_allowance(acct_info):
            return "counterparty receive pool does not have sufficient allowance"

        transfer_amount = bid_details.bid_size * bid_details.bid_price
        if acct_info.delegated_amount < transfer_amount:
            return "allowance is below required threshold"

        if acct_info.amount < transfer_amount:
            return "amount in token account is below required threshold"

        return None

    async def validate_bid(
        self, swap_order_creator: PublicKey, bid_details: BidDetails, signature: str
    ) -> Optional[str]:
        offer: Offer = await self.get_offer_details(swap_order_creator, bid_details.order_id)

        if bid_details.bid_size < offer.minBidSize:
            return "bid size is below min bid size"
        if bid_details.bid_size > offer.offerAmount:
            return "bid size is greater than offer size"
        if bid_details.bid_price < offer.minPrice:
            return "bid price is less than min price"

        if error_msg := await self._validate_bid_allowance(offer.biddingToken, bid_details):
            return error_msg

        if offer.expiry < int(time.time()):
            return "expiry was in the past"

        actual_signature = Signature.from_string(signature)

        message = bid_details.as_msg()

        verified = actual_signature.verify(bid_details.signer_wallet.to_solders(), message)

        if not verified:
            return "signature is invalid"

        # TODO: check mint of give pools and receive pools match

        return None

    async def create_offer(
        self, wallet: Wallet, template: SwapOrderTemplate
    ) -> Tuple[SwapOrder, PublicKey]:
        """
        Method to create offer
        Args:
            template (SwapOrderTemplate): template parameters to create
                a new offer
            wallet (Wallet): Wallet class instance
        Raises:
            TypeError: Offer argument is not a valid instance of Offer
                class
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
                "admin": GLOBAL_FRIKTION_ADMIN,
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
        acc = await self.get_swap_order_for_key(pdas.swap_order_address)

        await client.close()

        return (acc, pdas.swap_order_address)

    async def validate_and_exec_bid_msg(
        self,
        tx_sender_wallet: Wallet,
        swap_order_address: PublicKey,
        bid_details: BidDetails,
        signature: str,
    ):
        """
        Method to execute bid via signed message
        """
        swap_order = await self.get_swap_order_for_key(swap_order_address)

        if error := await self.validate_bid(swap_order.creator, bid_details, signature):
            raise ValueError(f'Invalid bid: {error}')

        counterparty_give_pool = get_associated_token_address(
            bid_details.signer_wallet, swap_order.give_mint
        )
        counterparty_receive_pool = get_associated_token_address(
            bid_details.signer_wallet, swap_order.receive_mint
        )

        ix = exec_msg(
   
            {
                "authority": tx_sender_wallet.public_key,
                "delegate_authority": DELEGATE_AUTHORITY_ADDRESS,
                "counterparty_wallet": bid_details.signer_wallet,
                "swap_order": swap_order_address,
                "give_pool": swap_order.give_pool,
                "receive_pool": swap_order.receive_pool,
                "counterparty_give_pool": counterparty_give_pool,
                "counterparty_receive_pool": counterparty_receive_pool,
                # pass in a dummy value since not using whitelisting
                # right now
                "whitelist_token_account": SYS_PROGRAM_ID,
                "instruction_sysvar": SYSVAR_INSTRUCTIONS_PUBKEY,
                "system_program": SYS_PROGRAM_ID,
                "token_program": TOKEN_PROGRAM_ID,
            },
        )

        tx = Transaction().add(ix)

        client = AsyncClient(self.url)
        await client.is_connected()

        provider = Provider(client, tx_sender_wallet)

        print('sending exec MSG tx...')
        tx_resp = await provider.send(tx, [])

        print(tx_resp)

        await client.confirm_transaction(tx_resp)
        await client.close()

    async def validate_and_exec_bid(
        self,
        wallet: Wallet,
        swap_order_address: PublicKey,
        bid_details: BidDetails,
        signature: str,
    ):
        """
        Method to validate bid
        Args:
        Returns:
            response (dict): Dictionary containing number of errors
                (errors) and the corresponding error messages (messages)
        """
        swap_order = await self.get_swap_order_for_key(swap_order_address)

        if error := await self.validate_bid(swap_order.creator, bid_details, signature):
            raise ValueError(f'Invalid bid: {error}')

        counterparty_give_pool = get_associated_token_address(
            bid_details.signer_wallet, swap_order.give_mint
        )
        counterparty_receive_pool = get_associated_token_address(
            bid_details.signer_wallet, swap_order.receive_mint
        )

        ix = exec(
            {
                "authority": bid_details.signer_wallet,
                "swap_order": swap_order_address,
                "give_pool": swap_order.give_pool,
                "receive_pool": swap_order.receive_pool,
                "counterparty_give_pool": counterparty_give_pool,
                "counterparty_receive_pool": counterparty_receive_pool,
                # pass in a dummy value since not using whitelisting
                # right now
                "whitelist_token_account": SYS_PROGRAM_ID,
                "system_program": SYS_PROGRAM_ID,
                "token_program": TOKEN_PROGRAM_ID,
            }
        )

        tx = Transaction().add(ix)

        client = AsyncClient(self.url)
        await client.is_connected()
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
            offer (dict): Offer dictionary containing necessary
                parameters to create a new offer
            wallet (Wallet): Wallet class instance
        Raises:
            TypeError: Offer argument is not a valid instance of Offer
                class
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
        acc = await self.get_swap_order_for_key(pdas.swap_order_address)

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
