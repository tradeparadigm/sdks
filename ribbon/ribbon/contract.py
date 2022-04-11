#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Steven@Ribbon, Paolo@Paradigm
# Created Date: 04/04/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Abstract class for contract connection """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import json
from web3 import Web3

from ribbon.chains import Chains
from ribbon.definitions import ContractConfig
from ribbon.utils import get_address


# ---------------------------------------------------------------------------
# Contract Connection
# ---------------------------------------------------------------------------
class ContractConnection:
    """
    Object to create connection to a contract

    Args:
        config (ContractConfig): Configuration to setup the Contract
        abi (str): Contract ABI location

    Attributes:
        address (str): Contract address
        abi (dict): Contract ABI
        w3 (object): RPC connection instance
        contract (object): Contract instance
    """

    abi_location = 'abis/Swap.json'

    def __init__(self, config: ContractConfig):
        if config.chain_name not in Chains:
            raise ValueError("Invalid chain")

        self.config = config
        self.address = get_address(self.config.address)

        self.w3 = Web3(Web3.HTTPProvider(self.config.rpc_uri))
        if not self.w3.isConnected():
            raise ValueError('RPC connection error')

        chain = self.config.chain_name
        rpc_chain_id = self.w3.eth.chain_id
        if int(rpc_chain_id) != chain.value:
            raise ValueError(
                f'RPC chain mismatched ({rpc_chain_id}). '
                + f'Expected: {chain.name} '
                + f'({chain.value})'
            )

        with open(self.abi_location) as f:
            abi = json.load(f)

        self.contract = self.w3.eth.contract(self.address, abi=abi)
