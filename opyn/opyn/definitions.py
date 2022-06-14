#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Anil@Opyn
# Created Date: 06/08/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module to store data classes """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from dataclasses import dataclass
from opyn.chains import Chains

# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------
@dataclass
class Domain:
    """
    Domain parameters for signatures

    # TODO: see if you can leverage this ID
    # to know which chain we are using
    # maybe to do in the smart contract itself
    # https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.chain_id
    """
    name: str
    version: int
    chainId: int
    verifyingContract: str

@dataclass
class MessageToSign:
    bidId: str
    trader: str
    token: str
    amount: str
    nonce: str 

@dataclass
class OrderData:
    bidId: str
    trader: str
    token: str
    amount: str
    v: str
    r: str
    s: str

@dataclass
class ContractConfig:
    """Configuration needed to connect to a Contract"""

    address: str
    rpc_uri: str
    chain_id: Chains = Chains.ETHEREUM
