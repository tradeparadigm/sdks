#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By: Steven@Ribbon
# Created Date: 04/04/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module to generate JWT signature """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import jwt

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ALGORITHM = 'EdDSA'

# ---------------------------------------------------------------------------
# Authenticator
# ---------------------------------------------------------------------------
class Authenticator:
  """
  Object to generate JWT signature

  Args:
      key (str): API key

  Attributes:
      key (str): API key in PKSI format
  """
  def __init__(self, key: str):
    self.key = '-----BEGIN PRIVATE KEY-----\n' \
      + key + '\n-----END PRIVATE KEY-----'

  def sign_jwt(self, payload: dict):
    """
    Method to generate JWT signature

    Args:
        payload (dict): payload to sign

    Returns:
        jwt (dict): JWT signature
    """
    return jwt.encode(payload, self.key, algorithm=ALGORITHM)
