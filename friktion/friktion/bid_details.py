import json
from dataclasses import dataclass
from typing import Tuple

from anchorpy import Wallet
from solana.publickey import PublicKey
from solders.signature import Signature


@dataclass
class BidDetails:
    signer_wallet: PublicKey
    order_id: int
    bid_size: int  # 1e9
    bid_price: int  # 1e9
    referrer: PublicKey

    def as_msg(self) -> bytes:
        give_amount = self.bid_size
        receive_amount = self.bid_price * self.bid_size * 10 ** 2
        print("receive amount = ", receive_amount)
        payload = bytearray()
        payload.extend(self.order_id.to_bytes(
            8,
            'little',
            signed = False
        ))
        payload.extend(self.signer_wallet.__bytes__())
        payload.extend(self.referrer.__bytes__())
        payload.extend(give_amount.to_bytes(8,'little',
                    signed = False
))
        payload.extend(receive_amount.to_bytes(
            8,'little',
                        signed = False

        ))
        
        return bytes(payload)
 
    def as_signed_msg(self, wallet: Wallet) -> Tuple[bytes, Signature]:
        msg_bytes = self.as_msg()
        return (msg_bytes, wallet.payer.sign(msg_bytes))
