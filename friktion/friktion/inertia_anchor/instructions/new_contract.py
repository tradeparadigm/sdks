from __future__ import annotations

import typing

import borsh_construct as borsh
from solana.publickey import PublicKey
from solana.transaction import AccountMeta, TransactionInstruction

from ..program_id import PROGRAM_ID


class NewContractArgs(typing.TypedDict):
    underlying_amount: int
    quote_amount: int
    expiry_ts: int
    is_call: int
    contract_bump: int
    option_bump: int
    writer_bump: int
    underlying_pool_bump: int
    claimable_pool_bump: int


layout = borsh.CStruct(
    "underlying_amount" / borsh.U64,
    "quote_amount" / borsh.U64,
    "expiry_ts" / borsh.U64,
    "is_call" / borsh.U64,
    "contract_bump" / borsh.U8,
    "option_bump" / borsh.U8,
    "writer_bump" / borsh.U8,
    "underlying_pool_bump" / borsh.U8,
    "claimable_pool_bump" / borsh.U8,
)


class NewContractAccounts(typing.TypedDict):
    payer: PublicKey
    admin_key: PublicKey
    oracle_ai: PublicKey
    contract: PublicKey
    writer_mint: PublicKey
    option_mint: PublicKey
    underlying_mint: PublicKey
    quote_mint: PublicKey
    underlying_pool: PublicKey
    claimable_pool: PublicKey
    mint_fee_account: PublicKey
    exercise_fee_account: PublicKey
    system_program: PublicKey
    token_program: PublicKey
    rent: PublicKey


def new_contract(args: NewContractArgs, accounts: NewContractAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["admin_key"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle_ai"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["contract"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["writer_mint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["option_mint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["underlying_mint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["quote_mint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["underlying_pool"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["claimable_pool"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["mint_fee_account"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["exercise_fee_account"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["system_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["token_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["rent"], is_signer=False, is_writable=False),
    ]
    identifier = b'\n\xd4,"c\x7f\xc3\x8f'
    encoded_args = layout.build(
        {
            "underlying_amount": args["underlying_amount"],
            "quote_amount": args["quote_amount"],
            "expiry_ts": args["expiry_ts"],
            "is_call": args["is_call"],
            "contract_bump": args["contract_bump"],
            "option_bump": args["option_bump"],
            "writer_bump": args["writer_bump"],
            "underlying_pool_bump": args["underlying_pool_bump"],
            "claimable_pool_bump": args["claimable_pool_bump"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
