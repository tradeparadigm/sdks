from __future__ import annotations

import typing

from solana.publickey import PublicKey
from solana.transaction import AccountMeta, TransactionInstruction

from ..program_id import PROGRAM_ID


class SetCounterpartyAccounts(typing.TypedDict):
    authority: PublicKey
    swap_order: PublicKey
    counterparty: PublicKey


def set_counterparty(accounts: SetCounterpartyAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["swap_order"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["counterparty"], is_signer=False, is_writable=False),
    ]
    identifier = b"\xda>\xcc@\xdf\x10\\\x87"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
