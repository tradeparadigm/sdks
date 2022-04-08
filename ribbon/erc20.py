#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By: Steven (steven@ribbon.finance)
# Created Date: 08/04/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module to interact with ERC20 contracts """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from web3 import Web3
from contract import ContractConnection
from utils import get_address

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DEFAULT_ABI_LOCATION = 'abis/ERC20.json'

# ---------------------------------------------------------------------------
# ERC20 Contract
# ---------------------------------------------------------------------------
class ERC20Contract(ContractConnection):
  """
  Object to create connection to an ERC20 contract

  Args:
      chain (str): The chain the contract is deployed in
      address (str): Contract address
      abi (dict): Contract ABI location
  """
  def __init__(
    self, 
    address: str,
    chain: str,
    abi: dict=DEFAULT_ABI_LOCATION
  ):
    super().__init__(address, chain, abi)
    self.decimals = self.contract.functions.decimals().call()

  def get_allowance(self, owner: str, spender: str) -> int:
    """
    Method to get allowance of owner

    Args:
        owner (str): Address of owner's address e.g. user wallet address
        spender (str): Address of spender's address e.g. the Swap contract

    Raises:
        ValueError: Address of wallet is invalid

    Returns:
        allowance (int): Amount owner approved for spender to use
    """
    owner_address = get_address(owner)
    spender_address = get_address(spender)
      
    response = self.contract.functions.allowance(
      owner_address, spender_address
    ).call()
    
    return response
  
  def get_balance(self, owner: str) -> int:
    """
    Method to get balance of owner

    Args:
        owner (str): Address of owner's address e.g. user wallet address

    Raises:
        ValueError: Address of wallet is invalid

    Returns:
        balance (int): Owner's balance
    """
    owner_address = get_address(owner)
      
    response = self.contract.functions.balanceOf(owner_address).call()
    
    return response