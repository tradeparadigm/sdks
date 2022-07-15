from typing import Union

from solana.publickey import PublicKey

from friktion.friktion_anchor.accounts.swap_order import SwapOrder


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
        minBidSize: int,
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
            swap_order.give_size,
        )
        o.swapOrderAddress = address
        return o
