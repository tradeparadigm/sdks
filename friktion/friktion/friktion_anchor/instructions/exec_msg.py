from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class ExecMsgAccounts(typing.TypedDict):
    authority: PublicKey
    delegate_authority: PublicKey
    swap_order: PublicKey
    counterparty_wallet: PublicKey
    give_pool: PublicKey
    receive_pool: PublicKey
    counterparty_receive_pool: PublicKey
    counterparty_give_pool: PublicKey
    whitelist_token_account: PublicKey
    instruction_sysvar: PublicKey
    system_program: PublicKey
    token_program: PublicKey


def exec_msg(accounts: ExecMsgAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["delegate_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["swap_order"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["counterparty_wallet"], is_signer=False, is_writable=False
        ),
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
            pubkey=accounts["instruction_sysvar"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"\xf8\x9d\x0f\xda\xc4\xb8\xf5\xb1"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
