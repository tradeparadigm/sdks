import typing
from anchorpy.error import ProgramError


class Unauthorized(ProgramError):
    def __init__(self) -> None:
        super().__init__(6000, "Unauthorized.")

    code = 6000
    name = "Unauthorized"
    msg = "Unauthorized."


class TooEarlyToExercise(ProgramError):
    def __init__(self) -> None:
        super().__init__(6001, "Invalid contract expiry.")

    code = 6001
    name = "TooEarlyToExercise"
    msg = "Invalid contract expiry."


class ContractExpired(ProgramError):
    def __init__(self) -> None:
        super().__init__(6002, "Options contract is expired.")

    code = 6002
    name = "ContractExpired"
    msg = "Options contract is expired."


class ContractNotYetExpired(ProgramError):
    def __init__(self) -> None:
        super().__init__(6003, "Cannot redeem until contract expiry.")

    code = 6003
    name = "ContractNotYetExpired"
    msg = "Cannot redeem until contract expiry."


class InvalidMultiplier(ProgramError):
    def __init__(self) -> None:
        super().__init__(6004, "Multiplier must be between 1 and 1000000")

    code = 6004
    name = "InvalidMultiplier"
    msg = "Multiplier must be between 1 and 1000000"


class InvalidFee(ProgramError):
    def __init__(self) -> None:
        super().__init__(6005, "Invalid fee")

    code = 6005
    name = "InvalidFee"
    msg = "Invalid fee"


class InvalidFeeOwner(ProgramError):
    def __init__(self) -> None:
        super().__init__(6006, "Invalid fee owner")

    code = 6006
    name = "InvalidFeeOwner"
    msg = "Invalid fee owner"


class InvalidQuoteTokenSource(ProgramError):
    def __init__(self) -> None:
        super().__init__(6007, "invalid quote token source")

    code = 6007
    name = "InvalidQuoteTokenSource"
    msg = "invalid quote token source"


class InvalidOptionTokenSource(ProgramError):
    def __init__(self) -> None:
        super().__init__(6008, "invalid option token source")

    code = 6008
    name = "InvalidOptionTokenSource"
    msg = "invalid option token source"


class InvalidWriterTokenSource(ProgramError):
    def __init__(self) -> None:
        super().__init__(6009, "invalid writer token source")

    code = 6009
    name = "InvalidWriterTokenSource"
    msg = "invalid writer token source"


class InvalidWriterTokenDestination(ProgramError):
    def __init__(self) -> None:
        super().__init__(6010, "invalid writer token destination")

    code = 6010
    name = "InvalidWriterTokenDestination"
    msg = "invalid writer token destination"


class InvalidUserUnderlyingTokens(ProgramError):
    def __init__(self) -> None:
        super().__init__(6011, "invalid user underlying tokens")

    code = 6011
    name = "InvalidUserUnderlyingTokens"
    msg = "invalid user underlying tokens"


class InvalidUserQuoteTokens(ProgramError):
    def __init__(self) -> None:
        super().__init__(6012, "invalid user quote tokens")

    code = 6012
    name = "InvalidUserQuoteTokens"
    msg = "invalid user quote tokens"


class InvalidContractUnderlyingPool(ProgramError):
    def __init__(self) -> None:
        super().__init__(6013, "invalid contract quote pool")

    code = 6013
    name = "InvalidContractUnderlyingPool"
    msg = "invalid contract quote pool"


class InvalidContractQuotePool(ProgramError):
    def __init__(self) -> None:
        super().__init__(6014, "invalid contract quote pool")

    code = 6014
    name = "InvalidContractQuotePool"
    msg = "invalid contract quote pool"


class InvalidOptionMint(ProgramError):
    def __init__(self) -> None:
        super().__init__(6015, "invalid option mint")

    code = 6015
    name = "InvalidOptionMint"
    msg = "invalid option mint"


class InvalidWriterMint(ProgramError):
    def __init__(self) -> None:
        super().__init__(6016, "invalid writer mint")

    code = 6016
    name = "InvalidWriterMint"
    msg = "invalid writer mint"


class InvalidUnderlyingMint(ProgramError):
    def __init__(self) -> None:
        super().__init__(6017, "invalid underlying mint")

    code = 6017
    name = "InvalidUnderlyingMint"
    msg = "invalid underlying mint"


class InvalidQuoteMint(ProgramError):
    def __init__(self) -> None:
        super().__init__(6018, "invalid quote mint")

    code = 6018
    name = "InvalidQuoteMint"
    msg = "invalid quote mint"


class InvalidUnderlyingOrQuoteAmount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6019, "invalid underlying or quote amount")

    code = 6019
    name = "InvalidUnderlyingOrQuoteAmount"
    msg = "invalid underlying or quote amount"


class RoundUnderlyingTokensMintDoesNotMatchVoltVault(ProgramError):
    def __init__(self) -> None:
        super().__init__(6020, "round underlying tokens does not match volt")

    code = 6020
    name = "RoundUnderlyingTokensMintDoesNotMatchVoltVault"
    msg = "round underlying tokens does not match volt"


class NotEnoughUnderlyingTokens(ProgramError):
    def __init__(self) -> None:
        super().__init__(6021, "not enough underlying tokens")

    code = 6021
    name = "NotEnoughUnderlyingTokens"
    msg = "not enough underlying tokens"


class NotEnoughWriterTokens(ProgramError):
    def __init__(self) -> None:
        super().__init__(6022, "not enough writer tokens")

    code = 6022
    name = "NotEnoughWriterTokens"
    msg = "not enough writer tokens"


class NotEnoughOptionTokens(ProgramError):
    def __init__(self) -> None:
        super().__init__(6023, "not enough option tokens")

    code = 6023
    name = "NotEnoughOptionTokens"
    msg = "not enough option tokens"


class MustBeNonZeroRedemption(ProgramError):
    def __init__(self) -> None:
        super().__init__(6024, "must be non zero # writer tokens being redeemed")

    code = 6024
    name = "MustBeNonZeroRedemption"
    msg = "must be non zero # writer tokens being redeemed"


class MustBeNonZeroWriteAmount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6025, "must be non zero write amount")

    code = 6025
    name = "MustBeNonZeroWriteAmount"
    msg = "must be non zero write amount"


class MustBeNonZeroExercise(ProgramError):
    def __init__(self) -> None:
        super().__init__(6026, "must be non zero exercise")

    code = 6026
    name = "MustBeNonZeroExercise"
    msg = "must be non zero exercise"


class NumberOverflow(ProgramError):
    def __init__(self) -> None:
        super().__init__(6027, "number overflow")

    code = 6027
    name = "NumberOverflow"
    msg = "number overflow"


class TooEarlyToExerciseContract(ProgramError):
    def __init__(self) -> None:
        super().__init__(6028, "too early to exercise contract")

    code = 6028
    name = "TooEarlyToExerciseContract"
    msg = "too early to exercise contract"


class TooEarlyToSettleContract(ProgramError):
    def __init__(self) -> None:
        super().__init__(6029, "too early to settle contract")

    code = 6029
    name = "TooEarlyToSettleContract"
    msg = "too early to settle contract"


class SettleWasNotCranked(ProgramError):
    def __init__(self) -> None:
        super().__init__(6030, "settle must be cranked")

    code = 6030
    name = "SettleWasNotCranked"
    msg = "settle must be cranked"


class NothingInClaimablePool(ProgramError):
    def __init__(self) -> None:
        super().__init__(6031, "nothing in claimable pool")

    code = 6031
    name = "NothingInClaimablePool"
    msg = "nothing in claimable pool"


class InvalidAuthorityForPermissionedInstruction(ProgramError):
    def __init__(self) -> None:
        super().__init__(6032, "Invalid authority for permissioned instruction")

    code = 6032
    name = "InvalidAuthorityForPermissionedInstruction"
    msg = "Invalid authority for permissioned instruction"


class TooLateToClosePosition(ProgramError):
    def __init__(self) -> None:
        super().__init__(6033, "Too late to close positiion")

    code = 6033
    name = "TooLateToClosePosition"
    msg = "Too late to close positiion"


class MustBeNonZeroClose(ProgramError):
    def __init__(self) -> None:
        super().__init__(6034, "must be non zero close position")

    code = 6034
    name = "MustBeNonZeroClose"
    msg = "must be non zero close position"


class OptionHasAlreadyBeenCranked(ProgramError):
    def __init__(self) -> None:
        super().__init__(6035, "option has already been cranked")

    code = 6035
    name = "OptionHasAlreadyBeenCranked"
    msg = "option has already been cranked"


class InvalidOracleType(ProgramError):
    def __init__(self) -> None:
        super().__init__(6036, "invalid oracle type")

    code = 6036
    name = "InvalidOracleType"
    msg = "invalid oracle type"


class InvalidOraclePrice(ProgramError):
    def __init__(self) -> None:
        super().__init__(6037, "invalid oracle price")

    code = 6037
    name = "InvalidOraclePrice"
    msg = "invalid oracle price"


class InvalidPythProgramId(ProgramError):
    def __init__(self) -> None:
        super().__init__(6038, "invalid pyth program id")

    code = 6038
    name = "InvalidPythProgramId"
    msg = "invalid pyth program id"


class PythExpoMustBeNegative(ProgramError):
    def __init__(self) -> None:
        super().__init__(6039, "pyth expo must be negative")

    code = 6039
    name = "PythExpoMustBeNegative"
    msg = "pyth expo must be negative"


class UlMintDoesntMatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6040, "ul mint doesn't match")

    code = 6040
    name = "UlMintDoesntMatch"
    msg = "ul mint doesn't match"


class QuoteMintDoesntMatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6041, "quote mint doesn't match")

    code = 6041
    name = "QuoteMintDoesntMatch"
    msg = "quote mint doesn't match"


class TooEarlyForNewContract(ProgramError):
    def __init__(self) -> None:
        super().__init__(6042, "too early for new contract")

    code = 6042
    name = "TooEarlyForNewContract"
    msg = "too early for new contract"


CustomError = typing.Union[
    Unauthorized,
    TooEarlyToExercise,
    ContractExpired,
    ContractNotYetExpired,
    InvalidMultiplier,
    InvalidFee,
    InvalidFeeOwner,
    InvalidQuoteTokenSource,
    InvalidOptionTokenSource,
    InvalidWriterTokenSource,
    InvalidWriterTokenDestination,
    InvalidUserUnderlyingTokens,
    InvalidUserQuoteTokens,
    InvalidContractUnderlyingPool,
    InvalidContractQuotePool,
    InvalidOptionMint,
    InvalidWriterMint,
    InvalidUnderlyingMint,
    InvalidQuoteMint,
    InvalidUnderlyingOrQuoteAmount,
    RoundUnderlyingTokensMintDoesNotMatchVoltVault,
    NotEnoughUnderlyingTokens,
    NotEnoughWriterTokens,
    NotEnoughOptionTokens,
    MustBeNonZeroRedemption,
    MustBeNonZeroWriteAmount,
    MustBeNonZeroExercise,
    NumberOverflow,
    TooEarlyToExerciseContract,
    TooEarlyToSettleContract,
    SettleWasNotCranked,
    NothingInClaimablePool,
    InvalidAuthorityForPermissionedInstruction,
    TooLateToClosePosition,
    MustBeNonZeroClose,
    OptionHasAlreadyBeenCranked,
    InvalidOracleType,
    InvalidOraclePrice,
    InvalidPythProgramId,
    PythExpoMustBeNegative,
    UlMintDoesntMatch,
    QuoteMintDoesntMatch,
    TooEarlyForNewContract,
]
CUSTOM_ERROR_MAP: dict[int, CustomError] = {
    6000: Unauthorized(),
    6001: TooEarlyToExercise(),
    6002: ContractExpired(),
    6003: ContractNotYetExpired(),
    6004: InvalidMultiplier(),
    6005: InvalidFee(),
    6006: InvalidFeeOwner(),
    6007: InvalidQuoteTokenSource(),
    6008: InvalidOptionTokenSource(),
    6009: InvalidWriterTokenSource(),
    6010: InvalidWriterTokenDestination(),
    6011: InvalidUserUnderlyingTokens(),
    6012: InvalidUserQuoteTokens(),
    6013: InvalidContractUnderlyingPool(),
    6014: InvalidContractQuotePool(),
    6015: InvalidOptionMint(),
    6016: InvalidWriterMint(),
    6017: InvalidUnderlyingMint(),
    6018: InvalidQuoteMint(),
    6019: InvalidUnderlyingOrQuoteAmount(),
    6020: RoundUnderlyingTokensMintDoesNotMatchVoltVault(),
    6021: NotEnoughUnderlyingTokens(),
    6022: NotEnoughWriterTokens(),
    6023: NotEnoughOptionTokens(),
    6024: MustBeNonZeroRedemption(),
    6025: MustBeNonZeroWriteAmount(),
    6026: MustBeNonZeroExercise(),
    6027: NumberOverflow(),
    6028: TooEarlyToExerciseContract(),
    6029: TooEarlyToSettleContract(),
    6030: SettleWasNotCranked(),
    6031: NothingInClaimablePool(),
    6032: InvalidAuthorityForPermissionedInstruction(),
    6033: TooLateToClosePosition(),
    6034: MustBeNonZeroClose(),
    6035: OptionHasAlreadyBeenCranked(),
    6036: InvalidOracleType(),
    6037: InvalidOraclePrice(),
    6038: InvalidPythProgramId(),
    6039: PythExpoMustBeNegative(),
    6040: UlMintDoesntMatch(),
    6041: QuoteMintDoesntMatch(),
    6042: TooEarlyForNewContract(),
}


def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err
