from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class RevertOptionSettleAccounts(typing.TypedDict):
    authority: PublicKey
    contract: PublicKey
    oracle_ai: PublicKey
    underlying_mint: PublicKey
    quote_mint: PublicKey
    contract_underlying_tokens: PublicKey
    claimable_pool: PublicKey
    exercise_fee_account: PublicKey
    token_program: PublicKey


def revert_option_settle(
    accounts: RevertOptionSettleAccounts,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["contract"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["oracle_ai"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["underlying_mint"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["quote_mint"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["contract_underlying_tokens"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["claimable_pool"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["exercise_fee_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"\xe5\xf0\xd6\x84j\xac*\x9f"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
