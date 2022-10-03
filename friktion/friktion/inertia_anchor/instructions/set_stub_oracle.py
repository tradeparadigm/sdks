from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class SetStubOracleArgs(typing.TypedDict):
    price: float


layout = borsh.CStruct("price" / borsh.F64)


class SetStubOracleAccounts(typing.TypedDict):
    authority: PublicKey
    stub_oracle: PublicKey
    system_program: PublicKey


def set_stub_oracle(
    args: SetStubOracleArgs, accounts: SetStubOracleAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["stub_oracle"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"\x95E\x02\x84\x8b\x89\xde\x1b"
    encoded_args = layout.build(
        {
            "price": args["price"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
