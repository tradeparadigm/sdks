import json
from pathlib import Path
from typing import Any

EVM_SIGNATURE_LEN = 130


def get_evm_signature_components(signature: str) -> tuple[str, str, int]:
    if len(signature) != EVM_SIGNATURE_LEN:
        raise ValueError(f'Invalid signature. Expected {EVM_SIGNATURE_LEN} character-long string')

    r = f'0x{signature[:64]}'
    s = f'0x{signature[64:128]}'
    v = int(signature[128:130], 16)

    return r, s, v


def get_abi_path(abi_name: str) -> Path:
    """
    Resolve an abi name to the absolute path of the abi json
    """
    return Path(__file__).parent.joinpath('abis', abi_name).with_suffix('.json')


def get_abi(abi_name: str) -> Any:
    """
    Resolve an abi name to the content of the abi json
    """
    abi_path = get_abi_path(abi_name)

    with open(abi_path) as f:
        return json.load(f)
