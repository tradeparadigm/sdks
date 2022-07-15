from __future__ import annotations

import typing

import borsh_construct as borsh
from anchorpy.borsh_extension import BorshPubkey
from solana.publickey import PublicKey
from solana.transaction import AccountMeta, TransactionInstruction

from ..program_id import PROGRAM_ID


class ExecMsgArgs(typing.TypedDict):
    signature: str
    caller: PublicKey
    raw_msg: str


layout = borsh.CStruct(
    "signature" / borsh.String, "caller" / BorshPubkey, "raw_msg" / borsh.String
)


class ExecMsgAccounts(typing.TypedDict):
    authority: PublicKey
    delegate_authority: PublicKey
    swap_order: PublicKey
    give_pool: PublicKey
    receive_pool: PublicKey
    counterparty_receive_pool: PublicKey
    counterparty_give_pool: PublicKey
    whitelist_token_account: PublicKey
    instruction_sysvar: PublicKey
    system_program: PublicKey
    token_program: PublicKey


def exec_msg(args: ExecMsgArgs, accounts: ExecMsgAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["delegate_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["swap_order"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["give_pool"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["receive_pool"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["counterparty_receive_pool"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["counterparty_give_pool"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["whitelist_token_account"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(pubkey=accounts["instruction_sysvar"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["system_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["token_program"], is_signer=False, is_writable=False),
    ]
    identifier = b"\xf8\x9d\x0f\xda\xc4\xb8\xf5\xb1"
    encoded_args = layout.build(
        {
            "signature": args["signature"],
            "caller": args["caller"],
            "raw_msg": args["raw_msg"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
