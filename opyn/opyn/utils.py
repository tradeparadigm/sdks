#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Anil@Opyn
# Created Date: 06/08/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Utility functions for encode.py """
# ---------------------------------------------------------------------------

from typing import Optional

from eth_typing import ChecksumAddress
from web3 import Web3

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PADDING = bytearray([0] * 32)
ADDRESS_ZERO = "0x0000000000000000000000000000000000000000"


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------
def id(text: str) -> str:
    """
    Generate the keccak256 of a string

    Args:
        text (str): String to hash

    Returns:
        hash (str): Resulting hash
    """
    return Web3.keccak(text=text).hex()


def get_address(address: Optional[str]) -> ChecksumAddress:
    """
    Validate address validity and return the checksum address

    Args:
        address (str): Address with 0x prefix

    Returns:
        address (ChecksumAddress): Returns address if valid
    """

    if not address:
        raise ValueError(f'Invalid address: {address}')

    try:
        return Web3.toChecksumAddress(address)
    except ValueError:
        raise ValueError(f'Invalid address: {address}')
