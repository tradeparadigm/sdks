from calendar import day_abbr
from friktion_swap_client.offer import Offer
from friktion_swap_client.swap import *
import time
import asyncio
from spl.token.async_client import AsyncToken
from friktion_swap_client.friktion_anchor.types.order_status import *
from solana.rpc.core import RPCException
from spl.token.instructions import get_associated_token_address

c = SwapContract(Network.DEVNET)

wallet = Wallet.local()


# devnet
GIVE_MINT = PublicKey("E6Z6zLzk8MWY3TY8E87mr88FhGowEPJTeMWzkqtL6qkF")
RECEIVE_MINT = PublicKey("C6kYXcaRUMqeBF5fhg165RWU7AnpT9z92fvKNoMqjmz6")

# make counterparty itself for purposes of testing
COUNTERPARTY = wallet.public_key
# dummy value for testing. not using whitelist tokens so shouldn't change much
WHITELIST_TOKEN_MINT = GIVE_MINT

OPTIONS_CONTRACT_KEY = PublicKey("GriGJSF84XdPq6Td6u6Hu8oqKgwTXY94fvwJrJf1gQTW")
# mainnet
# GIVE_MINT = PublicKey("")
# RECEIVE_MINT = PublicKey("")

async def main_def():

    client = AsyncClient(c.url)
    await client.is_connected()
    
    give_token = AsyncToken(
        client,
        GIVE_MINT,
        TOKEN_PROGRAM_ID,
        wallet.payer
    )
    receive_token = AsyncToken(
        client,
        RECEIVE_MINT,
        TOKEN_PROGRAM_ID,
        wallet.payer
    )

    ### create offer ###

    creator_give_pool_key = get_associated_token_address(
        wallet.public_key,
        GIVE_MINT
    )

    creator_receive_pool_key = get_associated_token_address(
        wallet.public_key,
        RECEIVE_MINT
    )

    counterparty_receive_pool_key = get_associated_token_address(
        wallet.public_key,
        RECEIVE_MINT
    )

    # create associated token accounts
    try:
        await give_token.create_associated_token_account(wallet.public_key)
    except RPCException as e:
        print('DEBUG: already created associated token account. Ignore this usually!\n e = {}'.format(e))

    try:
        await receive_token.create_associated_token_account(wallet.public_key)
    except RPCException as e:
        print('DEBUG: already created associated token account. Ignore this usually!\n e = {}'.format(e))
         

    try:
        print('current allowance: ', c.verify_allowance(wallet, RECEIVE_MINT, counterparty_receive_pool_key, True))
    except AssertionError:
        print("allowance needs to be delegated, doing...")
        c.give_allowance(wallet, counterparty_receive_pool_key, RECEIVE_MINT,  MIN_REQUIRED_ALLOWANCE)
        time.sleep(5.0)
        c.verify_allowance(wallet, RECEIVE_MINT, counterparty_receive_pool_key, True)

    print('1. creator initializes swap offer...')

    # create a dummy offer for testing purposes
    (swap_order_pre_fill, swap_order_key) = await c.create_offer(
        wallet, SwapOrderTemplate.from_offer(
            Offer(
                oToken=GIVE_MINT,
                biddingToken=RECEIVE_MINT,
                offerAmount=1,
                minPrice=0,
                minBidSize=1
            ), 
            OPTIONS_CONTRACT_KEY,
            1,
            int(time.time()) + 10000,
            creator_give_pool_key,
            COUNTERPARTY,
            True,
            False,
            WHITELIST_TOKEN_MINT,
        )
    )

    assert swap_order_pre_fill.status == Created()

    offer_pre_fill: Offer = await c.get_offer_details(
        wallet.public_key, swap_order_pre_fill.order_id
    )

    print('2. taker executes bid against offer...')

    bid_details =  BidDetails(
            wallet.public_key, swap_order_pre_fill.order_id,
            creator_give_pool_key,
            creator_receive_pool_key,
            1,
            1
        )
    # fill offer via bid
    await c.validate_bid(
        wallet,
        bid_details,
        swap_order_pre_fill,
        offer_pre_fill
    )

    bid_msg = bid_details.as_signed_msg(wallet, 1, 1)
    await c.validate_and_exec_bid_msg(wallet, bid_details, bid_msg, offer_pre_fill)

    offer_post_fill: Offer = await c.get_offer_details(
        wallet.public_key, swap_order_pre_fill.order_id
    )

    swap_order_post_fill: SwapOrder = await c.get_swap_order(
        wallet.public_key, swap_order_pre_fill.order_id
    )

    assert swap_order_post_fill.status == Filled()

    print(
        'otoken details =',
        await c.get_otoken_details_for_offer(offer_post_fill)
    )

    print('order post fill: {}'.format(swap_order_post_fill))

    print('3. creator reclaims assets...')

    await c.reclaim_assets_post_fill(wallet, swap_order_key, creator_give_pool_key, creator_receive_pool_key)
    print('Finished!')
    
    await client.close()
    
asyncio.run(main_def())