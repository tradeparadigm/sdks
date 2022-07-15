from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class OptionWriteArgs(typing.TypedDict):
    write_amount: int


layout = borsh.CStruct("write_amount" / borsh.U64)


class OptionWriteAccounts(typing.TypedDict):
    writer_authority: PublicKey
    contract: PublicKey
    user_underlying_funding_tokens: PublicKey
    underlying_pool: PublicKey
    writer_token_destination: PublicKey
    option_token_destination: PublicKey
    writer_mint: PublicKey
    option_mint: PublicKey
    fee_destination: PublicKey
    token_program: PublicKey
    clock: PublicKey


def option_write(
    args: OptionWriteArgs, accounts: OptionWriteAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["writer_authority"], is_signer=True, is_writable=True
        ),
        AccountMeta(pubkey=accounts["contract"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["user_underlying_funding_tokens"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["underlying_pool"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["writer_token_destination"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["option_token_destination"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["writer_mint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["option_mint"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["fee_destination"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["clock"], is_signer=False, is_writable=False),
    ]
    identifier = b"\xbd#\xdc\x18\xe0_r\x1b"
    encoded_args = layout.build(
        {
            "write_amount": args["write_amount"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
