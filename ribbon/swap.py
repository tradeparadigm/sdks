#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By: Steven (steven@ribbon.finance)
# Created Date: 04/04/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module to call Swap contract """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from web3 import Web3
from dataclasses import asdict
from contract import ContractConnection
from classes import SignedBid
from utils import get_address
from env import ADDRESSES

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DEFAULT_ABI_LOCATION = 'abis/Swap.json'

# ---------------------------------------------------------------------------
# Swap Contract
# ---------------------------------------------------------------------------
class SwapContract(ContractConnection):
  """
  Object to create connection to the Swap contract

  Args:
      chain (str): The chain the contract is deployed in
      abi (dict): Contract ABI location
  """
  def __init__(
    self,
    chain: str,
    abi: dict=DEFAULT_ABI_LOCATION
  ):
    address = ADDRESSES[chain]["swap"]["address"]

    super().__init__(address, chain, abi)

  def validate_bid(self, bid: SignedBid) -> str:
    """
    Method to validate bid

    Args:
        bid (dict): Bid dictionary containing swapId, nonce, signerWallet, 
          sellAmount, buyAmount, referrer, v, r, and s

    Raises:
        TypeError: Bid argument is not an instance of SignedBid

    Returns:
        response (dict): Dictionary containing number of errors (errors)
          and the corresponding error messages (messages)
    """
    if not isinstance(bid, SignedBid):
      raise TypeError("Invalid signed bid")

    bid.signerWallet = get_address(bid.signerWallet)
    bid.referrer = get_address(bid.referrer)

    response = self.contract.functions.check(asdict(bid)).call()
    
    errors = response[0]
    if errors == 0:
      return {'errors': 0}
    else:
      return {
        'errors': errors,
        'messages': [Web3.toText(msg).replace('\x00', '') 
          for msg in response[1][1:errors]
        ]
      }