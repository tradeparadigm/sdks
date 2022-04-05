#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By: Steven (steven@ribbon.finance)
# Created Date: 04/04/2022
# version ='0.01'
# ---------------------------------------------------------------------------
""" Module to call oToken contract """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from contract import ContractConnection

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DEFAULT_ABI_LOCATION = 'abis/oToken.json'

# ---------------------------------------------------------------------------
# oToken Contract
# ---------------------------------------------------------------------------
class oTokenContract(ContractConnection):
  """
  Object to create connection to the an oToken contract

  Args:
      rpc (str): Json RPC address to connect
      address (str): Contract address
      abi (dict): Contract ABI location
  """
  def __init__(self, rpc: str, address: str, abi: dict=DEFAULT_ABI_LOCATION):
        super().__init__(rpc, address, abi)

  def get_otoken_details(self) -> dict:
    """
    Method to validate bid

    Args:

    Returns:
        response (dict): Dictionary oToken details
    """
    details = self.contract.functions.getOtokenDetails().call()

    return {
      'collateralAsset': details[0], 
      'underlyingAsset': details[1], 
      'strikeAsset': details[2], 
      'strikePrice': details[3], 
      'expiryTimestamp': details[4], 
      'isPut': details[5]
    }