from __future__ import annotations

import typing

from solana.publickey import PublicKey
from solana.transaction import AccountMeta, TransactionInstruction

from ..program_id import PROGRAM_ID


class CancelAccounts(typing.TypedDict):
    authority: PublicKey
    swap_order: PublicKey
    creator_give_pool: PublicKey
    give_pool: PublicKey
    receive_pool: PublicKey
    token_program: PublicKey
    system_program: PublicKey


def cancel(accounts: CancelAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["swap_order"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["creator_give_pool"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["give_pool"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["receive_pool"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["token_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["system_program"], is_signer=False, is_writable=False),
    ]
    identifier = b"\xe8\xdb\xdf)\xdb\xec\xdc\xbe"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
