#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By: Steven (steven@ribbon.finance)
# Created Date: 04/04/2022
<<<<<<< main
# version ='0.1.0'
=======
# version ='0.01'
>>>>>>> main
# ---------------------------------------------------------------------------
""" Module to call Swap contract """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
<<<<<<< main
from web3 import Web3
from dataclasses import asdict
from contract import ContractConnection
from classes import SignedBid
from utils import get_address
from env import ADDRESSES
=======
from typing import Type
from web3 import Web3
from contract import ContractConnection
from classes import SignedBid
from dataclasses import asdict
>>>>>>> main

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
<<<<<<< main
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
=======
      rpc_url (str): Json RPC url to connect
      rpc_token (str): Json RPC url token
      address (str): Contract address
      abi (dict): Contract ABI location
  """
  def __init__(
    self, 
    rpc_url: str, 
    rpc_token: str, 
    address: str,
    abi: dict=DEFAULT_ABI_LOCATION
  ):
    super().__init__(rpc_url, rpc_token, address, abi)
>>>>>>> main

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

<<<<<<< main
    bid.signerWallet = get_address(bid.signerWallet)
    bid.referrer = get_address(bid.referrer)

=======
>>>>>>> main
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