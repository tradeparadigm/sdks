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

from chains import Chains, INFURA_RPC_URLS


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


@dataclass
class ContractConfig:
    """Configuration needed to connect to a Contract"""

    address: str
    infura_token: str
    bidding_token: str = None
    chain_name: Chains = Chains.TESTNET
    label: str = 'SwapContract'

    @property
    def infura_rpc_url(self):
        return INFURA_RPC_URLS[self.chain_name]
