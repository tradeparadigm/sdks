from dataclasses import dataclass
from typing import Tuple

from anchorpy import Wallet
from solana.publickey import PublicKey
from solders.signature import Signature

@dataclass
class BidDetails:
    signer_wallet: PublicKey
    order_id: int
    bid_size: int
    bid_price: int
    referrer: PublicKey

    def as_msg(self):
        give_amount = self.bid_size
        receive_amount = self.bid_price * self.bid_size
        byte_rep = b"".join(
            [
                bytes([self.order_id]),
                self.signer_wallet.__bytes__(),
                self.referrer.__bytes__(),
                bytes([give_amount, receive_amount]),
            ]
        )
        return byte_rep

    def as_signed_msg(self, wallet: Wallet) -> Tuple[bytes, Signature]:
        msg_bytes = self.as_msg()
        return (msg_bytes, wallet.payer.sign(msg_bytes))
