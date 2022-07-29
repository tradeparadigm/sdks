#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Steven@Ribbon
# Created Date: 04/04/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Utility functions for encode.py """
# ---------------------------------------------------------------------------

import re

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from web3 import Web3

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PADDING = bytearray([0] * 32)


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


def get_address(address: str) -> str:
    """
    Validate address validity and return the checksum address

    Args:
        address (str): Address with 0x prefix

    Returns:
        address (str): Returns address if valid
    """
    try:
        return Web3.toChecksumAddress(address)
    except ValueError:
        raise ValueError(f'Invalid address: {address}')


def hex_concat(items: list) -> str:
    """
    Concatenate list of hexes with 0x prefix

    Args:
        items (str): List of hexes with 0x prefix

    Returns:
        hex (str): Concatenated hex
    """
    return '0x' + ''.join([i[2:] for i in items])


def is_hex_string(value: str, length: int = None) -> bool:
    """
    Check if string is a hex with a specified length

    Args:
        value (str): Hex string
        length (int) (optional): Supposed length of hex

    Returns:
        isHex (bool): Boolean whether the given value is
          hex of a given length
    """
    if not isinstance(value, str) or not re.match('^0x[0-9A-Fa-f]*$', value):
        return False
    if length and len(value) != (2 + 2 * length):
        return False
    return True


def hex_zero_pad(value: str, length: int) -> str:
    """
    Add zero padding on the left

    Args:
        value (str): Hex string
        length (int): Desired hex length

    Returns:
        hex (object): Hex with padding
    """
    if not is_hex_string(value):
        raise ValueError(f'Invalid hex string: {value}')
    elif len(value) > 2 * length + 2:
        raise ValueError(f'Value out of range: {value}, {length}')

    while len(value) < 2 * length + 2:
        value = '0x0' + value[2:]

    return value


def hex_pad_right(value: str) -> str:
    """
    Add zero padding on the right to create hex of length 32

    Args:
        value (str): Hex string

    Returns:
        hex (object): Hex with padding
    """
    padOffset = len(value) % 32
    if padOffset > 0:
        return hex_concat([value, PADDING.hex()[padOffset:]])
    return value


def encode_type(name: str, fields: list) -> str:
    """
    Encode struct types

    Args:
        name (str): Name of struct
        fields (list): List of dictionary fields with name and type

    Returns:
        data (object): Encoded type
    """
    fields = ','.join([i['type'] + ' ' + i['name'] for i in fields])
    return f'{name}({fields})'
