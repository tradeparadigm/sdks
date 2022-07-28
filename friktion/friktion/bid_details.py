from dataclasses import dataclass
from typing import Tuple

from anchorpy import Wallet
from nacl import signing  # type: ignore
from solana.publickey import PublicKey
from solders.signature import Signature

@dataclass
class BidDetails:
    signer_wallet: PublicKey
    order_id: int
    bid_size: int
    bid_price: int
    referrer: PublicKey

    def as_signed_msg(self, wallet: Wallet) -> Tuple[bytes, Signature]:
        give_amount = self.bid_size
        receive_amount = self.bid_price * self.bid_size
        byte_rep = b"".join(
            [
                bytes([self.order_id]),
                wallet.public_key.__bytes__(),
                self.referrer.__bytes__(),
                bytes([give_amount, receive_amount]),
            ]
        )
        return (byte_rep, wallet.payer.sign(byte_rep))
