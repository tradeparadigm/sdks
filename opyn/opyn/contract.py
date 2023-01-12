#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Anil@Opyn
# Created Date: 06/08/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Abstract class for contract connection """
# ---------------------------------------------------------------------------

from web3 import Web3

from opyn.definitions import ContractConfig
from opyn.utils import get_address
from sdk_commons.helpers import get_abi


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

    def __init__(self, config: ContractConfig):

        # Can't be imported on top due to a circular dependency
        from opyn.config import OpynSDKConfig

        if config.chain_id not in OpynSDKConfig.supported_chains:
            raise ValueError("Invalid chain")

        self.config = config
        self.address = get_address(self.config.address)

        self.w3 = Web3(Web3.HTTPProvider(self.config.rpc_uri))
        if not self.w3.isConnected():
            raise ValueError("RPC connection error")

        chain = self.config.chain_id
        rpc_chain_id = self.w3.eth.chain_id
        if int(rpc_chain_id) != chain.value:
            raise ValueError(
                f"RPC chain mismatched ({rpc_chain_id}). "
                + f"Expected: {chain.name} "
                + f"({chain.value})"
            )

        # Note: Settlement.json is not included in common abis
        abi = get_abi('Settlement')

        self.contract = self.w3.eth.contract(self.address, abi=abi)
