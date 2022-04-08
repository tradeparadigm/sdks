#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By: Steven (steven@ribbon.finance)
# Created Date: 04/04/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module for wallet utilities """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import eth_keys
from dataclasses import asdict
from encode import TypedDataEncoder
from classes import Domain, Bid, SignedBid
from erc20 import ERC20Contract
from utils import get_address
from env import ADDRESSES

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
MIN_ALLOWANCE = 100000000

# ---------------------------------------------------------------------------
# Wallet Instance
# ---------------------------------------------------------------------------
class Wallet:
  """
  Object to generate bid signature

  Args:
      privateKey (str): Private key of the user in hex format with 0x prefix

  Attributes:
      signer (object): Instance of signer to generate signature
  """
  def __init__(self, privateKey: str) -> None:
    self.signer = eth_keys.keys.PrivateKey(bytes.fromhex(privateKey[2:]))
    self.address = get_address(self.signer.public_key.to_address())

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

  def _sign_type_data_v4(
    self, domain: Domain, value: dict, types: dict
  ) -> str:
    """Sign a hash of typed data V4 which follows EIP712 convention:
    https://eips.ethereum.org/EIPS/eip-712
    
    Args:
        domain (dict): Dictionary containing domain parameters including
          name, version, chainId, verifyingContract and salt (optional)
        types (dict): Dictionary of types and their fields
        value (dict): Dictionary of values for each field in types

    Raises:
        TypeError: Domain argument is not an instance of Domain class

    Returns:
        signature (dict): Signature split into v, r, s components
    """
    if not isinstance(domain, Domain):
      raise TypeError('Invalid domain parameters')

    domain_dict = {k: v for k, v in asdict(domain).items() if v is not None}

    return self.sign_msg(TypedDataEncoder._hash(domain_dict, types, value))

  def sign_bid(
    self, domain: Domain, bid: Bid, types: dict = BID_TYPES
  ) -> SignedBid:
    """Sign a bid using _sign_type_data_v4
    
    Args:
        domain (dict): Dictionary containing domain parameters including
          name, version, chainId, verifyingContract and salt (optional)
        types (dict): Dictionary of types and their fields
        bid (dict): Dicionary of bid specification

    Raises:
        TypeError: Bid argument is not an instance of Bid class

    Returns:
        signedBid (dict): Bid combined with the generated signature
    """
    if not isinstance(bid, Bid):
      raise TypeError('Invalid bid')

    signerWallet = get_address(bid.signerWallet)
    referrer = get_address(bid.referrer)

    if signerWallet != self.address:
      raise ValueError('Signer wallet address mismatch')

    signature = self._sign_type_data_v4(domain, asdict(bid), types)

    return SignedBid(
      swapId=bid.swapId,
      nonce=bid.nonce,
      signerWallet=signerWallet,
      sellAmount=bid.sellAmount,
      buyAmount=bid.buyAmount,
      referrer=referrer,
      v=signature['v'],
      r=signature['r'],
      s=signature['s']
    )

  def verify_wallet(self, vault: str, chain: str) -> str:
    """Verify wallet's allowance for a given vault
    
    Args:
        vault (str): Vault's address
        chain (str): Chain to verify wallet in

    Raises:
        ValueError: Address of vault is invalid

    Returns:
        verified (bool): True if wallet has sufficient allowance
    """

    if vault not in ADDRESSES[chain]["vaults"].keys():
      raise ValueError(f'Vault not found: {vault}')
    
    swap_address = ADDRESSES[chain]["swap"]["address"]
    bidding_token = ERC20Contract(
      ADDRESSES[chain]["vaults"][vault]["biddingToken"],
      chain=chain
    )
    
    allowance = bidding_token.get_allowance(self.address, swap_address) \
      / bidding_token.decimals

    return allowance > MIN_ALLOWANCE

