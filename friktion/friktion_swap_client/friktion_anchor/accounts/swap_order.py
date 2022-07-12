import typing
from dataclasses import dataclass
from base64 import b64decode
from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from anchorpy.borsh_extension import BorshPubkey
from ..program_id import PROGRAM_ID
from .. import types


class SwapOrderJSON(typing.TypedDict):
    creator: str
    price: float
    expiry: int
    give_size: int
    give_mint: str
    give_pool: str
    receive_size: int
    receive_mint: str
    receive_pool: str
    is_counterparty_provided: bool
    counterparty: str
    is_whitelisted: bool
    whitelist_token_mint: str
    is_disabled: bool
    status: types.order_status.OrderStatusJSON
    order_id: int
    options_contract: str
    bump: int


@dataclass
class SwapOrder:
    discriminator: typing.ClassVar = b"x\x00\xe4P\xa7\xf8I\xc9"
    layout: typing.ClassVar = borsh.CStruct(
        "creator" / BorshPubkey,
        "price" / borsh.F64,
        "expiry" / borsh.U64,
        "give_size" / borsh.U64,
        "give_mint" / BorshPubkey,
        "give_pool" / BorshPubkey,
        "receive_size" / borsh.U64,
        "receive_mint" / BorshPubkey,
        "receive_pool" / BorshPubkey,
        "is_counterparty_provided" / borsh.Bool,
        "counterparty" / BorshPubkey,
        "is_whitelisted" / borsh.Bool,
        "whitelist_token_mint" / BorshPubkey,
        "is_disabled" / borsh.Bool,
        "status" / types.order_status.layout,
        "order_id" / borsh.U64,
        "options_contract" / BorshPubkey,
        "bump" / borsh.U8,
    )
    creator: PublicKey
    price: float
    expiry: int
    give_size: int
    give_mint: PublicKey
    give_pool: PublicKey
    receive_size: int
    receive_mint: PublicKey
    receive_pool: PublicKey
    is_counterparty_provided: bool
    counterparty: PublicKey
    is_whitelisted: bool
    whitelist_token_mint: PublicKey
    is_disabled: bool
    status: types.order_status.OrderStatusKind
    order_id: int
    options_contract: PublicKey
    bump: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: PublicKey,
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.Optional["SwapOrder"]:
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
    ) -> typing.List[typing.Optional["SwapOrder"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["SwapOrder"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != PROGRAM_ID:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "SwapOrder":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = SwapOrder.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            creator=dec.creator,
            price=dec.price,
            expiry=dec.expiry,
            give_size=dec.give_size,
            give_mint=dec.give_mint,
            give_pool=dec.give_pool,
            receive_size=dec.receive_size,
            receive_mint=dec.receive_mint,
            receive_pool=dec.receive_pool,
            is_counterparty_provided=dec.is_counterparty_provided,
            counterparty=dec.counterparty,
            is_whitelisted=dec.is_whitelisted,
            whitelist_token_mint=dec.whitelist_token_mint,
            is_disabled=dec.is_disabled,
            status=types.order_status.from_decoded(dec.status),
            order_id=dec.order_id,
            options_contract=dec.options_contract,
            bump=dec.bump,
        )

    def to_json(self) -> SwapOrderJSON:
        return {
            "creator": str(self.creator),
            "price": self.price,
            "expiry": self.expiry,
            "give_size": self.give_size,
            "give_mint": str(self.give_mint),
            "give_pool": str(self.give_pool),
            "receive_size": self.receive_size,
            "receive_mint": str(self.receive_mint),
            "receive_pool": str(self.receive_pool),
            "is_counterparty_provided": self.is_counterparty_provided,
            "counterparty": str(self.counterparty),
            "is_whitelisted": self.is_whitelisted,
            "whitelist_token_mint": str(self.whitelist_token_mint),
            "is_disabled": self.is_disabled,
            "status": self.status.to_json(),
            "order_id": self.order_id,
            "options_contract": str(self.options_contract),
            "bump": self.bump,
        }

    @classmethod
    def from_json(cls, obj: SwapOrderJSON) -> "SwapOrder":
        return cls(
            creator=PublicKey(obj["creator"]),
            price=obj["price"],
            expiry=obj["expiry"],
            give_size=obj["give_size"],
            give_mint=PublicKey(obj["give_mint"]),
            give_pool=PublicKey(obj["give_pool"]),
            receive_size=obj["receive_size"],
            receive_mint=PublicKey(obj["receive_mint"]),
            receive_pool=PublicKey(obj["receive_pool"]),
            is_counterparty_provided=obj["is_counterparty_provided"],
            counterparty=PublicKey(obj["counterparty"]),
            is_whitelisted=obj["is_whitelisted"],
            whitelist_token_mint=PublicKey(obj["whitelist_token_mint"]),
            is_disabled=obj["is_disabled"],
            status=types.order_status.from_json(obj["status"]),
            order_id=obj["order_id"],
            options_contract=PublicKey(obj["options_contract"]),
            bump=obj["bump"],
        )
