import typing
from base64 import b64decode
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import BorshPubkey
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment

from ..program_id import PROGRAM_ID


class OptionsContractJSON(typing.TypedDict):
    admin_key: str
    oracle_ai: str
    underlying_mint: str
    quote_mint: str
    expiry_ts: int
    is_call: int
    contract_bump: int
    writer_bump: int
    underlying_pool_bump: int
    claimable_pool_bump: int
    option_bump: int
    underlying_amount: int
    quote_amount: int
    writer_mint: str
    option_mint: str
    underlying_pool: str
    claimable_pool: str
    mint_fee_account: str
    exercise_fee_account: str
    was_settle_cranked: bool
    extra_key1: str
    exercise_amount: int
    total_amount: int


@dataclass
class OptionsContract:
    discriminator: typing.ClassVar = b"#\xa8Zx\x88O%s"
    layout: typing.ClassVar = borsh.CStruct(
        "admin_key" / BorshPubkey,
        "oracle_ai" / BorshPubkey,
        "underlying_mint" / BorshPubkey,
        "quote_mint" / BorshPubkey,
        "expiry_ts" / borsh.U64,
        "is_call" / borsh.U64,
        "contract_bump" / borsh.U8,
        "writer_bump" / borsh.U8,
        "underlying_pool_bump" / borsh.U8,
        "claimable_pool_bump" / borsh.U8,
        "option_bump" / borsh.U8,
        "underlying_amount" / borsh.U64,
        "quote_amount" / borsh.U64,
        "writer_mint" / BorshPubkey,
        "option_mint" / BorshPubkey,
        "underlying_pool" / BorshPubkey,
        "claimable_pool" / BorshPubkey,
        "mint_fee_account" / BorshPubkey,
        "exercise_fee_account" / BorshPubkey,
        "was_settle_cranked" / borsh.Bool,
        "extra_key1" / BorshPubkey,
        "exercise_amount" / borsh.U64,
        "total_amount" / borsh.U64,
    )
    admin_key: PublicKey
    oracle_ai: PublicKey
    underlying_mint: PublicKey
    quote_mint: PublicKey
    expiry_ts: int
    is_call: int
    contract_bump: int
    writer_bump: int
    underlying_pool_bump: int
    claimable_pool_bump: int
    option_bump: int
    underlying_amount: int
    quote_amount: int
    writer_mint: PublicKey
    option_mint: PublicKey
    underlying_pool: PublicKey
    claimable_pool: PublicKey
    mint_fee_account: PublicKey
    exercise_fee_account: PublicKey
    was_settle_cranked: bool
    extra_key1: PublicKey
    exercise_amount: int
    total_amount: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: PublicKey,
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.Optional["OptionsContract"]:
        resp = await conn.get_account_info(address, commitment=commitment)
        info = resp["result"]["value"]
        if info is None:
            return None
        if info["owner"] != str(PROGRAM_ID):
            raise ValueError("Account does not belong to this program")
        bytes_data = b64decode(info["data"][0])
        return cls.decode(bytes_data)

    @classmethod
    async def fetch_multiple(
        cls,
        conn: AsyncClient,
        addresses: list[PublicKey],
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.List[typing.Optional["OptionsContract"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["OptionsContract"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != PROGRAM_ID:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "OptionsContract":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = OptionsContract.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            admin_key=dec.admin_key,
            oracle_ai=dec.oracle_ai,
            underlying_mint=dec.underlying_mint,
            quote_mint=dec.quote_mint,
            expiry_ts=dec.expiry_ts,
            is_call=dec.is_call,
            contract_bump=dec.contract_bump,
            writer_bump=dec.writer_bump,
            underlying_pool_bump=dec.underlying_pool_bump,
            claimable_pool_bump=dec.claimable_pool_bump,
            option_bump=dec.option_bump,
            underlying_amount=dec.underlying_amount,
            quote_amount=dec.quote_amount,
            writer_mint=dec.writer_mint,
            option_mint=dec.option_mint,
            underlying_pool=dec.underlying_pool,
            claimable_pool=dec.claimable_pool,
            mint_fee_account=dec.mint_fee_account,
            exercise_fee_account=dec.exercise_fee_account,
            was_settle_cranked=dec.was_settle_cranked,
            extra_key1=dec.extra_key1,
            exercise_amount=dec.exercise_amount,
            total_amount=dec.total_amount,
        )

    def to_json(self) -> OptionsContractJSON:
        return {
            "admin_key": str(self.admin_key),
            "oracle_ai": str(self.oracle_ai),
            "underlying_mint": str(self.underlying_mint),
            "quote_mint": str(self.quote_mint),
            "expiry_ts": self.expiry_ts,
            "is_call": self.is_call,
            "contract_bump": self.contract_bump,
            "writer_bump": self.writer_bump,
            "underlying_pool_bump": self.underlying_pool_bump,
            "claimable_pool_bump": self.claimable_pool_bump,
            "option_bump": self.option_bump,
            "underlying_amount": self.underlying_amount,
            "quote_amount": self.quote_amount,
            "writer_mint": str(self.writer_mint),
            "option_mint": str(self.option_mint),
            "underlying_pool": str(self.underlying_pool),
            "claimable_pool": str(self.claimable_pool),
            "mint_fee_account": str(self.mint_fee_account),
            "exercise_fee_account": str(self.exercise_fee_account),
            "was_settle_cranked": self.was_settle_cranked,
            "extra_key1": str(self.extra_key1),
            "exercise_amount": self.exercise_amount,
            "total_amount": self.total_amount,
        }

    @classmethod
    def from_json(cls, obj: OptionsContractJSON) -> "OptionsContract":
        return cls(
            admin_key=PublicKey(obj["admin_key"]),
            oracle_ai=PublicKey(obj["oracle_ai"]),
            underlying_mint=PublicKey(obj["underlying_mint"]),
            quote_mint=PublicKey(obj["quote_mint"]),
            expiry_ts=obj["expiry_ts"],
            is_call=obj["is_call"],
            contract_bump=obj["contract_bump"],
            writer_bump=obj["writer_bump"],
            underlying_pool_bump=obj["underlying_pool_bump"],
            claimable_pool_bump=obj["claimable_pool_bump"],
            option_bump=obj["option_bump"],
            underlying_amount=obj["underlying_amount"],
            quote_amount=obj["quote_amount"],
            writer_mint=PublicKey(obj["writer_mint"]),
            option_mint=PublicKey(obj["option_mint"]),
            underlying_pool=PublicKey(obj["underlying_pool"]),
            claimable_pool=PublicKey(obj["claimable_pool"]),
            mint_fee_account=PublicKey(obj["mint_fee_account"]),
            exercise_fee_account=PublicKey(obj["exercise_fee_account"]),
            was_settle_cranked=obj["was_settle_cranked"],
            extra_key1=PublicKey(obj["extra_key1"]),
            exercise_amount=obj["exercise_amount"],
            total_amount=obj["total_amount"],
        )
