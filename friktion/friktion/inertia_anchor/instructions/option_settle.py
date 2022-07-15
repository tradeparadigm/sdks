from __future__ import annotations

import typing

import borsh_construct as borsh
from solana.publickey import PublicKey
from solana.transaction import AccountMeta, TransactionInstruction

from ..program_id import PROGRAM_ID


class OptionSettleArgs(typing.TypedDict):
    settle_price: int
    bypass_code: int


layout = borsh.CStruct("settle_price" / borsh.U64, "bypass_code" / borsh.U64)


class OptionSettleAccounts(typing.TypedDict):
    authority: PublicKey
    contract: PublicKey
    oracle_ai: PublicKey
    underlying_mint: PublicKey
    quote_mint: PublicKey
    contract_underlying_tokens: PublicKey
    claimable_pool: PublicKey
    exercise_fee_account: PublicKey
    token_program: PublicKey
    clock: PublicKey


def option_settle(
    args: OptionSettleArgs, accounts: OptionSettleAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["contract"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["oracle_ai"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["underlying_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["quote_mint"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["contract_underlying_tokens"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["claimable_pool"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["exercise_fee_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["token_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["clock"], is_signer=False, is_writable=False),
    ]
    identifier = b"\xd4\xd9\xbc\xf1\x04\xfe=w"
    encoded_args = layout.build(
        {
            "settle_price": args["settle_price"],
            "bypass_code": args["bypass_code"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
