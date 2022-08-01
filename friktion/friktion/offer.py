from dataclasses import dataclass
from typing import Optional

from solana.publickey import PublicKey

from friktion.friktion_anchor.accounts.swap_order import SwapOrder


@dataclass
class Offer:
    oToken: PublicKey
    biddingToken: PublicKey
    expiry: int
    offerAmount: int  # 1, the smart contract always initializes option token with 0 decimals
    minPrice: int  # 1
    minBidSize: int  # 1, should match factor for offerAmount
    seller: PublicKey
    swapOrderAddress: Optional[PublicKey] = None

    @staticmethod
    def from_swap_order(swap_order: SwapOrder, address: PublicKey):
        return Offer(
            oToken=swap_order.give_mint,
            biddingToken=swap_order.receive_mint,
            expiry=swap_order.expiry,
            offerAmount=swap_order.give_size,
            minPrice=0,
            minBidSize=swap_order.give_size,
            swapOrderAddress=address,
            seller=swap_order.creator,
        )
