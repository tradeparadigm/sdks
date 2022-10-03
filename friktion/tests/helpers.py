import time

from anchorpy import Wallet
from asgiref.sync import async_to_sync
from solana.publickey import PublicKey
from spl.token.instructions import get_associated_token_address

from friktion.bid_details import BidDetails
from friktion.offer import Offer
from friktion.swap import MIN_REQUIRED_ALLOWANCE, Network, SwapContract
from friktion.swap_order_template import SwapOrderTemplate

SWAP_CONTRACT = SwapContract(Network.DEVNET)
TEST_BIDDING_TOKEN = PublicKey("C6kYXcaRUMqeBF5fhg165RWU7AnpT9z92fvKNoMqjmz6")
TEST_OFFERED_TOKEN = PublicKey("E6Z6zLzk8MWY3TY8E87mr88FhGowEPJTeMWzkqtL6qkF")
TEST_OPTIONS_CONTRACT = PublicKey("GriGJSF84XdPq6Td6u6Hu8oqKgwTXY94fvwJrJf1gQTW")


def give_allowance(bidding_token: PublicKey, wallet: Wallet):
    wallet_pub_key = wallet.public_key
    print(f'Giving allowance to {bidding_token=} on wallet={wallet_pub_key}')

    current_allowance, _ = SWAP_CONTRACT.get_allowance_and_amount(bidding_token, wallet_pub_key)
    has_min_allowance = SWAP_CONTRACT.verify_allowance(bidding_token, wallet_pub_key)
    print(f'{current_allowance=} / {has_min_allowance=}')

    SWAP_CONTRACT.give_allowance(wallet, bidding_token, MIN_REQUIRED_ALLOWANCE * 1000000)
    print('Waiting for transaction to propagate...')
    time.sleep(15)

    current_allowance, _ = SWAP_CONTRACT.get_allowance_and_amount(bidding_token, wallet_pub_key)
    has_min_allowance = SWAP_CONTRACT.verify_allowance(bidding_token, wallet_pub_key)
    print(f'{current_allowance=} / {has_min_allowance=}')


def create_offer(
    bidding_token: PublicKey,
    offered_token: PublicKey,
    swap_contract_addr: PublicKey,
    wallet: Wallet,
):
    creator_give_pool_key = get_associated_token_address(wallet.public_key, offered_token)
    order_template = SwapOrderTemplate.from_offer(
        offer=Offer(
            oToken=offered_token,
            biddingToken=bidding_token,
            expiry=int(time.time()) + 10000,
            offerAmount=10,
            minPrice=0,
            minBidSize=1,
            seller=wallet.public_key,
        ),
        options_contract=swap_contract_addr,
        receive_amount=1,
        creator_give_pool=creator_give_pool_key,
        counterparty=PublicKey('7yeeGWxusjqvjYGMSXuyYAdjqr13rJVL9WK2f2u7KbWV'),
        is_counterparty_provided=True,
    )
    order, order_addr = async_to_sync(SWAP_CONTRACT.create_offer)(wallet, order_template)
    print(f'Created offer: addr={order_addr} id={order.order_id} seller={order.creator}')


def execute_bid(
    wallet: Wallet,
    swap_order_addr: PublicKey,
    bid_details: BidDetails,
    signature: str,
):
    async_to_sync(SWAP_CONTRACT.validate_and_exec_bid_msg)(
        wallet, swap_order_addr, bid_details, signature
    )


if __name__ == "__main__":
    # Make sure you loaded the correct wallet
    wallet = Wallet.local()
    print(f'Loaded wallet: {wallet.public_key}')

    # ------ Use maker wallet ------
    # Give Allowance
    # give_allowance(TEST_BIDDING_TOKEN, wallet)

    # ------ Use taker wallet ------
    # Create Offer
    create_offer(TEST_BIDDING_TOKEN, TEST_OFFERED_TOKEN, TEST_OPTIONS_CONTRACT, wallet)

    # Execute Bid
    swap_order_addr = PublicKey('Gv6avmZYFjSCjL2ofRzRrNSQqAngLUM1uAjrpLzwSuMG')
    bid_details = BidDetails(
        bid_price=500000,
        bid_size=10,
        order_id=22,
        creator=wallet.public_key,
        referrer=PublicKey('7yeeGWxusjqvjYGMSXuyYAdjqr13rJVL9WK2f2u7KbWV'),
        signer_wallet=PublicKey('7yeeGWxusjqvjYGMSXuyYAdjqr13rJVL9WK2f2u7KbWV'),
    )
    signature = "5Yg2oyQCKd7hxtnNwWXkGBUKBMpzB9AZu6zcrM4yc45Q1WpEEuEbZK7HASmwtP8E5ABydQn2aHhMt5Cj7QbDxb4x"  # noqa
    # execute_bid(wallet, swap_order_addr, bid_details, signature)
