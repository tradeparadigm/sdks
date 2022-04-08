#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By: Steven (steven@ribbon.finance)
# Created Date: 04/04/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module to store data classes """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------
@dataclass
class Domain:
  """Domain parameters for signatures"""
  name: str
  chainId: int
  verifyingContract: str
  version: int
  salt: str = None

@dataclass
class Bid:
  """Bid parameters"""
  swapId: int
  nonce: int
  signerWallet: str
  sellAmount: int
  buyAmount: int
  referrer: str

@dataclass
class SignedBid(Bid):
  """Signed bid fields"""
  v: int
  r: str
  s: str