import json
from dataclasses import dataclass
from typing import Tuple

from anchorpy import Wallet
from solana.publickey import PublicKey
from solders.signature import Signature


@dataclass
class BidDetails:
    signer_wallet: PublicKey
    swap_order_addr: PublicKey
    order_id: int
    bid_size: int
    bid_price: int
    referrer: PublicKey

    def as_msg(self):
        give_amount = self.bid_size
        receive_amount = self.bid_price * self.bid_size
        payload = [
            [self.order_id],
            str(
                self.swap_order_addr
            ),  # TODO: temp change to allow testing. We need to wait for the PR from Friktion
            str(self.signer_wallet),
            str(self.referrer),
            [give_amount, receive_amount],
        ]

        # set separators to remove whitespaces
        dumped_payload = json.dumps(payload, separators=(',', ':'))

        return bytes(dumped_payload, 'utf-8')

    def as_signed_msg(self, wallet: Wallet) -> Tuple[bytes, Signature]:
        msg_bytes = self.as_msg()
        return (msg_bytes, wallet.payer.sign(msg_bytes))
