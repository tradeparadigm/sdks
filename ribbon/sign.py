#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By: Steven (steven@ribbon.finance)
# Created Date: 04/04/2022
# version ='0.01'
# ---------------------------------------------------------------------------
""" Module to generate signature to bid """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import eth_keys
from encode import TypedDataEncoder
from classes import Domain, Bid, SignedBid

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BID_TYPES = {
    'Bid': [
      {'name': 'swapId', 'type': 'uint256'},
      {'name': 'nonce', 'type': 'uint256'},
      {'name': 'signerWallet', 'type': 'address'},
      {'name': 'sellAmount', 'type': 'uint256'},
      {'name': 'buyAmount', 'type': 'uint256'},
      {'name': 'referrer', 'type': 'address'},
    ]
  }

# ---------------------------------------------------------------------------
# Signature Generator
# ---------------------------------------------------------------------------
class Signature:
  """
  Object to generate bid signature

  Args:
      privateKey (str): Private key of the user in hex format with 0x prefix

  Attributes:
      signer (object): Instance of signer to generate signature
  """
  def __init__(self, privateKey: str) -> None:
    self.signer = eth_keys.keys.PrivateKey(bytes.fromhex(privateKey[2:]))

  def sign_msg(self, messageHash: str) -> dict:
    """Sign a hash message using the signer object

    Args:
        messageHash (str): Message to signed in hex format with 0x prefix

    Returns:
        signature (dict): Signature split into v, r, s components
    """
    signature = self.signer.sign_msg_hash(bytes.fromhex(messageHash[2:]))

    return {
      'v': signature.v + 27,
      'r': hex(signature.r),
      's': hex(signature.s)
    }

  def _sign_type_data_v4(self, domain: Domain, value: dict, types: dict) -> str:
    """Sign a hash of typed data V4 which follows EIP712 convention:
    https://eips.ethereum.org/EIPS/eip-712
    
    Args:
        domain (dict): Dictionary containing domain parameters including
          name, version, chainId, verifyingContract and salt (optional)
        types (dict): Dictionary of types and their fields
        value (dict): Dictionary of values for each field in types

    Returns:
        signature (dict): Signature split into v, r, s components
    """
    return self.sign_msg(TypedDataEncoder._hash(domain, types, value))

  def sign_bid(self, domain: Domain, bid: Bid, types: dict = BID_TYPES) -> SignedBid:
    """Sign a bid using _sign_type_data_v4
    
    Args:
        domain (dict): Dictionary containing domain parameters including
          name, version, chainId, verifyingContract and salt (optional)
        types (dict): Dictionary of types and their fields
        bid (dict): Dicionary of bid specification

    Returns:
        signedBid (dict): Bid combined with the generated signature
    """
    signature = self._sign_type_data_v4(domain, bid, types)

    return {
      'swapId': bid['swapId'],
      'nonce': bid['nonce'],
      'signerWallet': bid['signerWallet'],
      'sellAmount': bid['sellAmount'],
      'buyAmount': bid['buyAmount'],
      'referrer': bid['referrer'],
      'v': signature['v'],
      'r': signature['r'],
      's': signature['s']
    }

