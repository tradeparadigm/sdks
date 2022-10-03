from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class ExecAccounts(typing.TypedDict):
    authority: PublicKey
    swap_order: PublicKey
    give_pool: PublicKey
    receive_pool: PublicKey
    counterparty_receive_pool: PublicKey
    counterparty_give_pool: PublicKey
    whitelist_token_account: PublicKey
    system_program: PublicKey
    token_program: PublicKey


def exec(accounts: ExecAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["swap_order"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["give_pool"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["receive_pool"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["counterparty_receive_pool"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["counterparty_give_pool"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["whitelist_token_account"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"2\x10s3\xa8z9-"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
