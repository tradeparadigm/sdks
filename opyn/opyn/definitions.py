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
    version: str
    chainId: int
    verifyingContract: str

@dataclass
class MessageToSign:
    offerId: int
    bidId: int
    signerAddress: str
    bidderAddress: str
    bidToken: str
    offerToken: str
    bidAmount: int
    sellAmount: int
    nonce: int 

@dataclass
class BidData:
    offerId: int
    bidId: int
    signerAddress: str
    bidderAddress: str
    bidToken: str
    offerToken: str
    bidAmount: int
    sellAmount: int
    v: int
    r: str
    s: str

@dataclass
class TestToSign:
    offerId: int
    bidId: int

@dataclass
class TestData:
    offerId: int
    bidId: int
    v: int
    r: str
    s: str

@dataclass
class ContractConfig:
    """Configuration needed to connect to a Contract"""
    address: str
    rpc_uri: str
    chain_id: Chains = Chains.ETHEREUM

@dataclass
class Offer:
    """On-chain offer"""
    offerToken: str
    bidToken: str
    minPrice: int
    minBidSize: int
    totalSize: int
