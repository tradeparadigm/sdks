import typing
from anchorpy.error import ProgramError


class InvalidCounterParty(ProgramError):
    def __init__(self) -> None:
        super().__init__(6000, "invalid counter party")

    code = 6000
    name = "InvalidCounterParty"
    msg = "invalid counter party"


class InvalidGivePool(ProgramError):
    def __init__(self) -> None:
        super().__init__(6001, "invalid give pool")

    code = 6001
    name = "InvalidGivePool"
    msg = "invalid give pool"


class InvalidReceivePool(ProgramError):
    def __init__(self) -> None:
        super().__init__(6002, "invalid receive pool")

    code = 6002
    name = "InvalidReceivePool"
    msg = "invalid receive pool"


class CounterpartyMustBeSigner(ProgramError):
    def __init__(self) -> None:
        super().__init__(6003, "counterparty must be signer")

    code = 6003
    name = "CounterpartyMustBeSigner"
    msg = "counterparty must be signer"


class SwapOrderWasFilled(ProgramError):
    def __init__(self) -> None:
        super().__init__(6004, "swap order was filled")

    code = 6004
    name = "SwapOrderWasFilled"
    msg = "swap order was filled"


class SwapOrderWasCanceled(ProgramError):
    def __init__(self) -> None:
        super().__init__(6005, "swap order was canceled")

    code = 6005
    name = "SwapOrderWasCanceled"
    msg = "swap order was canceled"


class SwapOrderIsDisabled(ProgramError):
    def __init__(self) -> None:
        super().__init__(6006, "swap order is disabled")

    code = 6006
    name = "SwapOrderIsDisabled"
    msg = "swap order is disabled"


class SwapOrderHasExpired(ProgramError):
    def __init__(self) -> None:
        super().__init__(6007, "swap order has expired")

    code = 6007
    name = "SwapOrderHasExpired"
    msg = "swap order has expired"


class SwapOrderMustBeDisabledToClose(ProgramError):
    def __init__(self) -> None:
        super().__init__(6008, "swap order must be disabled to close")

    code = 6008
    name = "SwapOrderMustBeDisabledToClose"
    msg = "swap order must be disabled to close"


class OrderAlreadyFilled(ProgramError):
    def __init__(self) -> None:
        super().__init__(6009, "order already filled")

    code = 6009
    name = "OrderAlreadyFilled"
    msg = "order already filled"


class OrderAlreadyCancelled(ProgramError):
    def __init__(self) -> None:
        super().__init__(6010, "order already cancelled")

    code = 6010
    name = "OrderAlreadyCancelled"
    msg = "order already cancelled"


class InvalidWhitelistTokenAccountMint(ProgramError):
    def __init__(self) -> None:
        super().__init__(6011, "invalid whitelist token account mint")

    code = 6011
    name = "InvalidWhitelistTokenAccountMint"
    msg = "invalid whitelist token account mint"


class MustHaveAtLeastOneMarketMakerAccessToken(ProgramError):
    def __init__(self) -> None:
        super().__init__(6012, "min 1 mm token")

    code = 6012
    name = "MustHaveAtLeastOneMarketMakerAccessToken"
    msg = "min 1 mm token"


class ReceivePoolMustBeEmpty(ProgramError):
    def __init__(self) -> None:
        super().__init__(6013, "receive pool must be empty")

    code = 6013
    name = "ReceivePoolMustBeEmpty"
    msg = "receive pool must be empty"


class GivePoolMustBeEmpty(ProgramError):
    def __init__(self) -> None:
        super().__init__(6014, "give pool must be empty")

    code = 6014
    name = "GivePoolMustBeEmpty"
    msg = "give pool must be empty"


class OrderMustBeFilled(ProgramError):
    def __init__(self) -> None:
        super().__init__(6015, "order must be filled")

    code = 6015
    name = "OrderMustBeFilled"
    msg = "order must be filled"


class OrderMustBeTrading(ProgramError):
    def __init__(self) -> None:
        super().__init__(6016, "order must be trading")

    code = 6016
    name = "OrderMustBeTrading"
    msg = "order must be trading"


class InvalidEd25519Program(ProgramError):
    def __init__(self) -> None:
        super().__init__(6017, "invalid ed25519 program")

    code = 6017
    name = "InvalidEd25519Program"
    msg = "invalid ed25519 program"


class InvalidSwapAdmin(ProgramError):
    def __init__(self) -> None:
        super().__init__(6018, "invalid swap admin")

    code = 6018
    name = "InvalidSwapAdmin"
    msg = "invalid swap admin"


class InvalidEd25519InstructionData(ProgramError):
    def __init__(self) -> None:
        super().__init__(6019, "")

    code = 6019
    name = "InvalidEd25519InstructionData"
    msg = ""


class OptionAndGiveMintDontMatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6020, "option and give mint don't match")

    code = 6020
    name = "OptionAndGiveMintDontMatch"
    msg = "option and give mint don't match"


CustomError = typing.Union[
    InvalidCounterParty,
    InvalidGivePool,
    InvalidReceivePool,
    CounterpartyMustBeSigner,
    SwapOrderWasFilled,
    SwapOrderWasCanceled,
    SwapOrderIsDisabled,
    SwapOrderHasExpired,
    SwapOrderMustBeDisabledToClose,
    OrderAlreadyFilled,
    OrderAlreadyCancelled,
    InvalidWhitelistTokenAccountMint,
    MustHaveAtLeastOneMarketMakerAccessToken,
    ReceivePoolMustBeEmpty,
    GivePoolMustBeEmpty,
    OrderMustBeFilled,
    OrderMustBeTrading,
    InvalidEd25519Program,
    InvalidSwapAdmin,
    InvalidEd25519InstructionData,
    OptionAndGiveMintDontMatch,
]
CUSTOM_ERROR_MAP: dict[int, CustomError] = {
    6000: InvalidCounterParty(),
    6001: InvalidGivePool(),
    6002: InvalidReceivePool(),
    6003: CounterpartyMustBeSigner(),
    6004: SwapOrderWasFilled(),
    6005: SwapOrderWasCanceled(),
    6006: SwapOrderIsDisabled(),
    6007: SwapOrderHasExpired(),
    6008: SwapOrderMustBeDisabledToClose(),
    6009: OrderAlreadyFilled(),
    6010: OrderAlreadyCancelled(),
    6011: InvalidWhitelistTokenAccountMint(),
    6012: MustHaveAtLeastOneMarketMakerAccessToken(),
    6013: ReceivePoolMustBeEmpty(),
    6014: GivePoolMustBeEmpty(),
    6015: OrderMustBeFilled(),
    6016: OrderMustBeTrading(),
    6017: InvalidEd25519Program(),
    6018: InvalidSwapAdmin(),
    6019: InvalidEd25519InstructionData(),
    6020: OptionAndGiveMintDontMatch(),
}


def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err
