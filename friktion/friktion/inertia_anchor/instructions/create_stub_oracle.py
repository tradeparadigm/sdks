from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class CreateStubOracleArgs(typing.TypedDict):
    price: float
    pda_str: str


layout = borsh.CStruct("price" / borsh.F64, "pda_str" / borsh.String)


class CreateStubOracleAccounts(typing.TypedDict):
    authority: PublicKey
    stub_oracle: PublicKey
    system_program: PublicKey
    rent: PublicKey


def create_stub_oracle(
    args: CreateStubOracleArgs, accounts: CreateStubOracleAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["stub_oracle"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["rent"], is_signer=False, is_writable=False),
    ]
    identifier = b"\x85u1\x0cx\xf4\xd8\xdb"
    encoded_args = layout.build(
        {
            "price": args["price"],
            "pda_str": args["pda_str"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
