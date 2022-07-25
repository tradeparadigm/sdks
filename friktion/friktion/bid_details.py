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

    def as_signed_msg(
        self, wallet: Wallet, receive_amount: int, give_amount: int
    ) -> signing.SignedMessage:
        byte_rep = b"".join(
            [
                bytes([self.order_id]),
                wallet.public_key.__bytes__(),
                bytes([give_amount, receive_amount]),
            ]
        )
        return wallet.payer.sign(byte_rep)
