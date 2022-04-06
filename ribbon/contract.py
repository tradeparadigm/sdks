#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By: Steven (steven@ribbon.finance)
# Created Date: 04/04/2022
# version ='0.01'
# ---------------------------------------------------------------------------
""" Abstract class for contract connection """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from web3 import Web3
import json
import os

# ---------------------------------------------------------------------------
# Contract Connection
# ---------------------------------------------------------------------------
class ContractConnection:
  """
  Object to create connection to a contract

  Args:
      rpc_url (str): Json RPC url to connect
      rpc_token (str): Json RPC url token
      address (str): Contract address
      abi (dict): Contract ABI location

  Attributes:
      address (str): Contract address
      abi (dict): Contract ABI
      w3 (object): RPC connection instance
      contract (object): Contract instance
  """
  def __init__(self, rpc_url: str, rpc_token: str, address: str, abi: dict) -> None:
    self.address = address
    self.abi = abi
    self.w3 = Web3(Web3.HTTPProvider(os.path.join(rpc_url + rpc_token)))

    if not self.w3.isConnected():
      raise ValueError('RPC connection error')

    with open(self.abi) as f:
      self.abi = json.load(f)

    self.contract = self.w3.eth.contract(self.address, abi=self.abi)