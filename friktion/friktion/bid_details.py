from anchorpy import Wallet
from nacl import signing  # type: ignore
from solana.publickey import PublicKey

from friktion.pda import SwapOrderAddresses


class BidDetails:

    swap_order_owner: PublicKey
    order_id: int

    counterparty_give_pool: PublicKey
    counterparty_receive_pool: PublicKey

    bid_size: int

    def __init__(
        self,
        swap_order_owner: PublicKey,
        order_id: int,
        counterparty_give_pool: PublicKey,
        counterparty_receive_pool: PublicKey,
        bid_size: int,
        bid_price: int,
    ):
        self.swap_order_owner = swap_order_owner
        self.order_id = order_id
        self.counterparty_give_pool = counterparty_give_pool
        self.counterparty_receive_pool = counterparty_receive_pool
        self.bid_size = bid_size
        self.bid_price = bid_price

    def get_swap_order_address(self) -> PublicKey:
        return (SwapOrderAddresses(self.swap_order_owner, self.order_id)).swap_order_address

    def as_signed_msg(
        self, wallet: Wallet, receive_amount: int, give_amount: int
    ) -> signing.SignedMessage:
        byte_rep = b"".join(
            [
                bytes([self.order_id]),
                wallet.public_key.__bytes__(),
                bytes(
                    [
                        give_amount,
                        receive_amount,
                    ]
                ),
            ]
        )
        return wallet.payer.sign(byte_rep)
