import asyncio
import time

from anchorpy import Wallet
from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient
from solana.rpc.core import RPCException
from spl.token.async_client import AsyncToken
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import get_associated_token_address

from friktion.bid_details import BidDetails
from friktion.friktion_anchor.accounts.swap_order import SwapOrder
from friktion.friktion_anchor.types.order_status import Created, Filled
from friktion.offer import Offer
from friktion.swap import MIN_REQUIRED_ALLOWANCE, Network, SwapContract
from friktion.swap_order_template import SwapOrderTemplate

c = SwapContract(Network.DEVNET)

wallet = Wallet.local()


# devnet
GIVE_MINT = PublicKey("E6Z6zLzk8MWY3TY8E87mr88FhGowEPJTeMWzkqtL6qkF")
RECEIVE_MINT = PublicKey("C6kYXcaRUMqeBF5fhg165RWU7AnpT9z92fvKNoMqjmz6")

# make counterparty itself for purposes of testing
COUNTERPARTY = wallet.public_key
# dummy value for testing. not using whitelist tokens so shouldn't
# change much
WHITELIST_TOKEN_MINT = GIVE_MINT

OPTIONS_CONTRACT_KEY = PublicKey("GriGJSF84XdPq6Td6u6Hu8oqKgwTXY94fvwJrJf1gQTW")
# mainnet
# GIVE_MINT = PublicKey("")
# RECEIVE_MINT = PublicKey("")


async def main_def():

    client = AsyncClient(c.url)
    await client.is_connected()

    give_token = AsyncToken(client, GIVE_MINT, TOKEN_PROGRAM_ID, wallet.payer)
    receive_token = AsyncToken(client, RECEIVE_MINT, TOKEN_PROGRAM_ID, wallet.payer)

    # create offer
    creator_give_pool_key = get_associated_token_address(wallet.public_key, GIVE_MINT)
    creator_receive_pool_key = get_associated_token_address(wallet.public_key, RECEIVE_MINT)

    # create associated token accounts
    try:
        await give_token.create_associated_token_account(wallet.public_key)
    except RPCException as e:
        print(f'DEBUG: already created associated token account. Ignore this usually!\n{e=}')

    try:
        await receive_token.create_associated_token_account(wallet.public_key)
    except RPCException as e:
        print(f'DEBUG: already created associated token account. Ignore this usually!\n{e=}')

    print('current allowance: ', c.get_allowance_and_amount(RECEIVE_MINT, COUNTERPARTY))

    if not c.verify_allowance(RECEIVE_MINT, COUNTERPARTY):
        print("allowance needs to be delegated, doing...")
        c.give_allowance(wallet, RECEIVE_MINT, MIN_REQUIRED_ALLOWANCE)
        print("Sleeping waiting for allowance to be propagated")
        time.sleep(15.0)
        assert c.verify_allowance(
            RECEIVE_MINT, COUNTERPARTY
        ), 'Give allowance transaction took look then expected. Please run the program again.'

    print('1. creator initializes swap offer...')
    # create a dummy offer for testing purposes
    (swap_order_pre_fill, swap_order_key) = await c.create_offer(
        wallet,
        SwapOrderTemplate.from_offer(
            Offer(
                oToken=GIVE_MINT,
                biddingToken=RECEIVE_MINT,
                expiry=int(time.time()) + 10000,
                offerAmount=1,
                minPrice=0,
                minBidSize=1,
                seller=wallet.public_key,
            ),
            OPTIONS_CONTRACT_KEY,
            1,
            creator_give_pool_key,
            COUNTERPARTY,
            True,
            False,
            WHITELIST_TOKEN_MINT,
        ),
    )

    assert swap_order_pre_fill.status == Created()
    order_id = swap_order_pre_fill.order_id
    swap_order_creator = swap_order_pre_fill.creator

    offer_pre_fill: Offer = await c.get_offer_details(swap_order_creator, order_id)
    print(f'order post fill: {offer_pre_fill}')

    offered_token_details = await c.get_offered_token_details(swap_order_creator, order_id)
    print(f'otoken details = {offered_token_details}')

    print('2. taker executes bid against offer...')
    bid_details = BidDetails(
        bid_price=1,
        bid_size=1,
        order_id=order_id,
        signer_wallet=COUNTERPARTY,
    )
    # fill offer via bid
    if error := await c.validate_bid(swap_order_creator, bid_details):
        raise ValueError(f'Invalid bid: {error}')

    bid_msg = bid_details.as_signed_msg(wallet, 1, 1)
    await c.validate_and_exec_bid_msg(wallet, swap_order_key, bid_details, bid_msg)

    swap_order_post_fill: SwapOrder = await c.get_swap_order(swap_order_creator, order_id)
    assert swap_order_post_fill.status == Filled()
    print(f'order post fill: {swap_order_post_fill}')

    print('3. creator reclaims assets...')

    await c.reclaim_assets_post_fill(
        wallet, swap_order_key, creator_give_pool_key, creator_receive_pool_key
    )
    print('Finished!')

    await client.close()


asyncio.run(main_def())
