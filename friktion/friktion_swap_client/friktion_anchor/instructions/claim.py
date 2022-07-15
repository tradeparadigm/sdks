from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class ClaimAccounts(typing.TypedDict):
    authority: PublicKey
    swap_order: PublicKey
    creator_give_pool: PublicKey
    creator_receive_pool: PublicKey
    give_pool: PublicKey
    receive_pool: PublicKey
    token_program: PublicKey
    system_program: PublicKey


def claim(accounts: ClaimAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["swap_order"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["creator_give_pool"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["creator_receive_pool"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["give_pool"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["receive_pool"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b">\xc6\xd6\xc1\xd5\x9fl\xd2"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
