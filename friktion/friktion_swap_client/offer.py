from typing import Union
from friktion_swap_client.friktion_anchor.accounts.swap_order import SwapOrder
from solana.publickey import PublicKey
class Offer(object):
    oToken: PublicKey
    biddingToken: PublicKey
    offerAmount: int
    minPrice: int
    minBidSize: int
    swapOrderAddress: Union[PublicKey, None]

    def __init__(
        self,
        oToken: PublicKey,
        biddingToken: PublicKey,
        offerAmount: int,
        minPrice: int,
        minBidSize: int
    ):
        self.oToken = oToken
        self.biddingToken = biddingToken
        self.offerAmount = offerAmount
        self.minPrice = minPrice
        self.minBidSize = minBidSize

        self.swapOrderAddress = None

    @staticmethod
    def from_swap_order(swap_order: SwapOrder, address: PublicKey):
        o = Offer(
            swap_order.give_mint,
            swap_order.receive_mint,
            swap_order.give_size,
            0,
            swap_order.give_size
        )
        o.swapOrderAddress = address
        return o