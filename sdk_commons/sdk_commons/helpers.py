EVM_SIGNATURE_LEN = 130


def get_evm_signature_components(signature: str) -> tuple[str, str, int]:
    if len(signature) != EVM_SIGNATURE_LEN:
        raise ValueError(f'Invalid signature. Expected {EVM_SIGNATURE_LEN} character-long string')

    r = f'0x{signature[:64]}'
    s = f'0x{signature[64:128]}'
    v = int(signature[128:130], 16)

    return r, s, v
