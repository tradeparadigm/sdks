import typing
from base64 import b64decode
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment

from ..program_id import PROGRAM_ID


class StubOracleJSON(typing.TypedDict):
    magic: int
    price: float
    last_update: int
    pda_str: str


@dataclass
class StubOracle:
    discriminator: typing.ClassVar = b"\xe0\xfb\xfec\xb1\xae\x89\x04"
    layout: typing.ClassVar = borsh.CStruct(
        "magic" / borsh.U32,
        "price" / borsh.F64,
        "last_update" / borsh.I64,
        "pda_str" / borsh.String,
    )
    magic: int
    price: float
    last_update: int
    pda_str: str

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: PublicKey,
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.Optional["StubOracle"]:
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
    ) -> typing.List[typing.Optional["StubOracle"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["StubOracle"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != PROGRAM_ID:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "StubOracle":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = StubOracle.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            magic=dec.magic,
            price=dec.price,
            last_update=dec.last_update,
            pda_str=dec.pda_str,
        )

    def to_json(self) -> StubOracleJSON:
        return {
            "magic": self.magic,
            "price": self.price,
            "last_update": self.last_update,
            "pda_str": self.pda_str,
        }

    @classmethod
    def from_json(cls, obj: StubOracleJSON) -> "StubOracle":
        return cls(
            magic=obj["magic"],
            price=obj["price"],
            last_update=obj["last_update"],
            pda_str=obj["pda_str"],
        )
