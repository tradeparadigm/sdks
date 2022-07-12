from typing import Tuple
import solders.signature as signature
from anchorpy import Wallet
from numpy import rec
from solana.publickey import PublicKey
import sys
from nacl import signing  # type: ignore
from .friktion_anchor.accounts import SwapOrder, UserOrders
from .friktion_anchor.program_id import PROGRAM_ID
from .friktion_anchor.instructions import create
from solana.rpc.async_api import AsyncClient
from .constants import WHITELIST_TOKEN_MINT
class BidDetails():

    swap_order_owner: PublicKey
    order_id: int

    counterparty_give_pool: PublicKey
    counterparty_receive_pool: PublicKey

    bid_size: int

    def __init__(self,
        swap_order_owner: PublicKey,
        order_id: int,
        counterparty_give_pool: PublicKey,
        counterparty_receive_pool: PublicKey,
        bid_size: int,
        bid_price: int
    ):
        self.swap_order_owner = swap_order_owner
        self.order_id = order_id
        self.counterparty_give_pool = counterparty_give_pool
        self.counterparty_receive_pool = counterparty_receive_pool
        self.bid_size = bid_size
        self.bid_price = bid_price

    def as_signed_msg(self, wallet: Wallet, receive_amount: int, give_amount: int) -> signing.SignedMessage:
        byte_rep = b"".join([bytes([
            self.order_id
        ]),wallet.public_key.to_base58(),bytes([
            give_amount,
            receive_amount,
        ])])
        return wallet.payer.sign(
            byte_rep
        )

    # deprecated implementation for older version of solanapy
    # def as_signed_msg(self, wallet: Wallet, receive_amount: int, give_amount: int) -> Tuple[bytes, signature.Signature]:
    #     byte_rep = b"".join([bytes([
    #         self.order_id
    #     ]),wallet.public_key.to_base58(),bytes([
    #         give_amount,
    #         receive_amount,
    #     ])])
    #     return (byte_rep, wallet.payer.sign(
    #         byte_rep
    #     ))