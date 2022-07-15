from __future__ import annotations

import typing

import borsh_construct as borsh
from solana.publickey import PublicKey
from solana.transaction import AccountMeta, TransactionInstruction

from ..program_id import PROGRAM_ID


class ClosePositionArgs(typing.TypedDict):
    num_contracts: int


layout = borsh.CStruct("num_contracts" / borsh.U64)


class ClosePositionAccounts(typing.TypedDict):
    close_authority: PublicKey
    contract: PublicKey
    writer_mint: PublicKey
    option_mint: PublicKey
    option_token_source: PublicKey
    writer_token_source: PublicKey
    underlying_token_destination: PublicKey
    underlying_pool: PublicKey
    token_program: PublicKey
    clock: PublicKey


def close_position(
    args: ClosePositionArgs, accounts: ClosePositionAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["close_authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["contract"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["writer_mint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["option_mint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["option_token_source"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["writer_token_source"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["underlying_token_destination"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["underlying_pool"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["token_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["clock"], is_signer=False, is_writable=False),
    ]
    identifier = b"{\x86Q\x001Dbb"
    encoded_args = layout.build(
        {
            "num_contracts": args["num_contracts"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
