from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class OptionRedeemArgs(typing.TypedDict):
    num_contracts: int


layout = borsh.CStruct("num_contracts" / borsh.U64)


class OptionRedeemAccounts(typing.TypedDict):
    redeemer_authority: PublicKey
    contract: PublicKey
    writer_token_source: PublicKey
    writer_mint: PublicKey
    contract_underlying_tokens: PublicKey
    underlying_token_destination: PublicKey
    token_program: PublicKey


def option_redeem(
    args: OptionRedeemArgs, accounts: OptionRedeemAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["redeemer_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(pubkey=accounts["contract"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["writer_token_source"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["writer_mint"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["contract_underlying_tokens"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["underlying_token_destination"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"\x14\x0c\xaa\x94\x11\x81XZ"
    encoded_args = layout.build(
        {
            "num_contracts": args["num_contracts"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
