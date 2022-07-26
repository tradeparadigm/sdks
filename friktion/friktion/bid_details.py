from dataclasses import dataclass

from anchorpy import Wallet
from nacl import signing  # type: ignore
from solana.publickey import PublicKey


@dataclass
class BidDetails:
    signer_wallet: PublicKey
    order_id: int
    bid_size: int
    bid_price: int

    def as_signed_msg(self, wallet: Wallet) -> signing.SignedMessage:
        buy_amount = self.bid_size
        sell_amount = self.bid_price * self.bid_size
        byte_rep = b"".join(
            [
                bytes([self.order_id]),
                wallet.public_key.__bytes__(),
                bytes([buy_amount, sell_amount]),
            ]
        )
        return wallet.payer.sign(byte_rep)
