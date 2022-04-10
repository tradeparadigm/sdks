#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Steven (steven@ribbon.finance)
# Created Date: 04/04/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module to store data classes """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from dataclasses import dataclass
from meta import BaseEnum


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------
@dataclass
class Domain:
    """Domain parameters for signatures"""

    name: str
    chainId: int
    verifyingContract: str
    version: int
    salt: str = None


@dataclass
class Bid:
    swapId: int
    signerWallet: str
    sellAmount: int
    buyAmount: int
    nonce: int = 1
    referrer: str = "0x0000000000000000000000000000000000000000"


@dataclass
class SignedBid(Bid):
    v: int = None
    r: str = None
    s: str = None


class Chains(BaseEnum):
    ETHEREUM_PROD = "mainnet"
    ETHEREUM_TESTNET = "kovan"
    AVALANCHE_PROD = "c-chain"
    AVALANCHE_TESTNET = "fuji"


@dataclass
class ContractConfig:
    """Configuration needed to connect to a Contract"""

    address: str
    rpc_uri: str
    bidding_token: str = None
    chain_name: Chains = Chains.ETHEREUM_TESTNET
    label: str = 'SwapContract'

    def __post_init__(self):
        """Validate attributes"""
        if self.chain_name not in Chains:
            raise AttributeError(f"Invalid chain: {self.chain_name}")
