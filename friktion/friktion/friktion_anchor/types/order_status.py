from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import EnumForCodegen


class CreatedJSON(typing.TypedDict):
    kind: typing.Literal["Created"]


class CanceledJSON(typing.TypedDict):
    kind: typing.Literal["Canceled"]


class FilledJSON(typing.TypedDict):
    kind: typing.Literal["Filled"]


class DisabledJSON(typing.TypedDict):
    kind: typing.Literal["Disabled"]


@dataclass
class Created:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Created"

    @classmethod
    def to_json(cls) -> CreatedJSON:
        return CreatedJSON(
            kind="Created",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Created": {},
        }


@dataclass
class Canceled:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Canceled"

    @classmethod
    def to_json(cls) -> CanceledJSON:
        return CanceledJSON(
            kind="Canceled",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Canceled": {},
        }


@dataclass
class Filled:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "Filled"

    @classmethod
    def to_json(cls) -> FilledJSON:
        return FilledJSON(
            kind="Filled",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Filled": {},
        }


@dataclass
class Disabled:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "Disabled"

    @classmethod
    def to_json(cls) -> DisabledJSON:
        return DisabledJSON(
            kind="Disabled",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Disabled": {},
        }


OrderStatusKind = typing.Union[Created, Canceled, Filled, Disabled]
OrderStatusJSON = typing.Union[CreatedJSON, CanceledJSON, FilledJSON, DisabledJSON]


def from_decoded(obj: dict) -> OrderStatusKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Created" in obj:
        return Created()
    if "Canceled" in obj:
        return Canceled()
    if "Filled" in obj:
        return Filled()
    if "Disabled" in obj:
        return Disabled()
    raise ValueError("Invalid enum object")


def from_json(obj: OrderStatusJSON) -> OrderStatusKind:
    if obj["kind"] == "Created":
        return Created()
    if obj["kind"] == "Canceled":
        return Canceled()
    if obj["kind"] == "Filled":
        return Filled()
    if obj["kind"] == "Disabled":
        return Disabled()

    # This statement is unreachable, all cases of
    # OrderStatusJSON are already verified
    kind = obj["kind"]  # type: ignore
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Created" / borsh.CStruct(),
    "Canceled" / borsh.CStruct(),
    "Filled" / borsh.CStruct(),
    "Disabled" / borsh.CStruct(),
)
