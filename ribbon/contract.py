#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By: Steven (steven@ribbon.finance)
# Created Date: 04/04/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Abstract class for contract connection """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import json
import os
from utils import get_address
from web3 import Web3
from env import CHAINS, RPCS

# ---------------------------------------------------------------------------
# Contract Connection
# ---------------------------------------------------------------------------
class ContractConnection:
  """
  Object to create connection to a contract

  Args:
      chain (str): The chain the contract is deployed in
      address (str): Contract address
      abi (dict): Contract ABI location

  Attributes:
      address (str): Contract address
      abi (dict): Contract ABI
      w3 (object): RPC connection instance
      contract (object): Contract instance
  """
  def __init__(self, address: str, chain: str, abi: dict) -> None:
    self.chain = chain

    if self.chain not in CHAINS:
      raise ValueError("Invalid chain")

    url, token = RPCS[chain].values()
    
    self.address = get_address(address)
    self.abi = abi
    self.w3 = Web3(Web3.HTTPProvider(os.path.join(url + token)))

    if not self.w3.isConnected():
      raise ValueError('RPC connection error')

    with open(self.abi) as f:
      self.abi = json.load(f)

    self.contract = self.w3.eth.contract(self.address, abi=self.abi)