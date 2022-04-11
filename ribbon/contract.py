#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
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
from utils import get_address
from web3 import Web3
from definitions import ContractConfig


# ---------------------------------------------------------------------------
# Contract Connection
# ---------------------------------------------------------------------------
class ContractConnection:
    """
    Object to create connection to a contract

    Args:
        config (ContractConfig): configuration to setup the Contract
        abi (str): Contract ABI location

    Attributes:
        address (str): Contract address
        abi (dict): Contract ABI
        w3 (object): RPC connection instance
        contract (object): Contract instance
    """

    abi_location = "abis/Swap.json"

    def __init__(self, config: ContractConfig):
        self.config = config
        self.address = get_address(self.config.address)

        self.w3 = Web3(Web3.HTTPProvider(self.config.rpc_uri))
        if not self.w3.isConnected():
            raise ValueError("RPC connection error")

        with open(self.abi_location) as f:
            abi = json.load(f)

        self.contract = self.w3.eth.contract(self.address, abi=abi)
