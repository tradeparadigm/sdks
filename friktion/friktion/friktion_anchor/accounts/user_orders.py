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


class UserOrdersJSON(typing.TypedDict):
    user: str
    curr_order_id: int


@dataclass
class UserOrders:
    discriminator: typing.ClassVar = b" CbS.\x05\x06\x91"
    layout: typing.ClassVar = borsh.CStruct("user" / BorshPubkey, "curr_order_id" / borsh.U64)
    user: PublicKey
    curr_order_id: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: PublicKey,
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.Optional["UserOrders"]:
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
    ) -> typing.List[typing.Optional["UserOrders"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["UserOrders"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != PROGRAM_ID:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "UserOrders":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = UserOrders.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            user=dec.user,
            curr_order_id=dec.curr_order_id,
        )

    def to_json(self) -> UserOrdersJSON:
        return {
            "user": str(self.user),
            "curr_order_id": self.curr_order_id,
        }

    @classmethod
    def from_json(cls, obj: UserOrdersJSON) -> "UserOrders":
        return cls(
            user=PublicKey(obj["user"]),
            curr_order_id=obj["curr_order_id"],
        )
