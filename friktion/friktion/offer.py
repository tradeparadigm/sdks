from typing import Optional

from solana.publickey import PublicKey

from friktion.friktion_anchor.accounts.swap_order import SwapOrder


class Offer(object):
    oToken: PublicKey
    biddingToken: PublicKey
    offerAmount: int
    minPrice: int
    minBidSize: int
    swapOrderAddress: Optional[PublicKey]

    def __init__(
        self,
        oToken: PublicKey,
        biddingToken: PublicKey,
        offerAmount: int,
        minPrice: int,
        minBidSize: int,
        swapOrderAddress: PublicKey = None,
    ):
        self.oToken = oToken
        self.biddingToken = biddingToken
        self.offerAmount = offerAmount
        self.minPrice = minPrice
        self.minBidSize = minBidSize
        self.swapOrderAddress = swapOrderAddress

    @staticmethod
    def from_swap_order(swap_order: SwapOrder, address: PublicKey):
        return Offer(
            swap_order.give_mint,
            swap_order.receive_mint,
            swap_order.give_size,
            0,
            swap_order.give_size,
            swapOrderAddress=address,
        )
