#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By: Anil@Opyn
# Created Date: 06/08/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Utility functions for encode.py """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from web3 import Web3
import re

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PADDING = bytearray([0] * 32)

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

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
  elif (len(value) > 2 * length + 2):
    raise ValueError(f'Value out of range: {value}, {length}')

  while (len(value) < 2 * length + 2):
    value = '0x0' + value[2:]

  return value
