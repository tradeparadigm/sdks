import json
from dataclasses import dataclass
from typing import Tuple

from anchorpy import Wallet
from solana.publickey import PublicKey
from solders.signature import Signature

from friktion.pda import find_swap_order_address


@dataclass
class BidDetails:
    signer_wallet: PublicKey
    # necessary to verify swap order public key
    creator: PublicKey
    order_id: int
    bid_size: int  # 1e9
    bid_price: int  # 1e9
    referrer: PublicKey

    def as_msg(self) -> bytes:
        give_amount = self.bid_size
        receive_amount = self.bid_price * self.bid_size
        payload = bytearray()
        payload.extend(self.order_id.to_bytes(
            8,
            'little',
            signed = False
        ))
        swap_order_pk = find_swap_order_address(self.creator, self.order_id)[0]
        payload.extend(self.signer_wallet.__bytes__())
        payload.extend(self.referrer.__bytes__())
        payload.extend(swap_order_pk.__bytes__())
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
