from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class OptionExerciseArgs(typing.TypedDict):
    num_contracts: int


layout = borsh.CStruct("num_contracts" / borsh.U64)


class OptionExerciseAccounts(typing.TypedDict):
    exerciser_authority: PublicKey
    contract: PublicKey
    option_mint: PublicKey
    option_token_source: PublicKey
    underlying_token_destination: PublicKey
    claimable_pool: PublicKey
    token_program: PublicKey


def option_exercise(
    args: OptionExerciseArgs, accounts: OptionExerciseAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["exerciser_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(pubkey=accounts["contract"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["option_mint"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["option_token_source"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["underlying_token_destination"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["claimable_pool"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"+V\xedN\xebJ\x83\xce"
    encoded_args = layout.build(
        {
            "num_contracts": args["num_contracts"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
