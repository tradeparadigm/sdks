from __future__ import annotations

import typing

import borsh_construct as borsh
from solana.publickey import PublicKey
from solana.transaction import AccountMeta, TransactionInstruction

from ..program_id import PROGRAM_ID


class CreateArgs(typing.TypedDict):
    give_size: int
    receive_size: int
    expiry: int
    is_counterparty_provided: bool
    is_whitelisted: bool
    enforce_mint_match: bool


layout = borsh.CStruct(
    "give_size" / borsh.U64,
    "receive_size" / borsh.U64,
    "expiry" / borsh.U64,
    "is_counterparty_provided" / borsh.Bool,
    "is_whitelisted" / borsh.Bool,
    "enforce_mint_match" / borsh.Bool,
)


class CreateAccounts(typing.TypedDict):
    payer: PublicKey
    authority: PublicKey
    user_orders: PublicKey
    swap_order: PublicKey
    give_pool: PublicKey
    give_mint: PublicKey
    receive_pool: PublicKey
    receive_mint: PublicKey
    creator_give_pool: PublicKey
    counterparty: PublicKey
    whitelist_token_mint: PublicKey
    options_contract: PublicKey
    system_program: PublicKey
    token_program: PublicKey
    rent: PublicKey


def create(args: CreateArgs, accounts: CreateAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["payer"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["user_orders"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["swap_order"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["give_pool"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["give_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["receive_pool"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["receive_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["creator_give_pool"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["counterparty"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["whitelist_token_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["options_contract"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["system_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["token_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["rent"], is_signer=False, is_writable=False),
    ]
    identifier = b"\x18\x1e\xc8(\x05\x1c\x07w"
    encoded_args = layout.build(
        {
            "give_size": args["give_size"],
            "receive_size": args["receive_size"],
            "expiry": args["expiry"],
            "is_counterparty_provided": args["is_counterparty_provided"],
            "is_whitelisted": args["is_whitelisted"],
            "enforce_mint_match": args["enforce_mint_match"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
