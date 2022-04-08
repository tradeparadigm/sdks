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
    nonce: int
    signerWallet: str
    sellAmount: int
    buyAmount: int
    referrer: str


@dataclass
class SignedBid(Bid):
    v: int
    r: str
    s: str


@dataclass
class ContractDetails:
    address: str
    bidding_token: str = None


@dataclass
class ContractConfig:
    """Configuration needed to connect to a Contract"""

    details: ContractDetails
    infura_token: str
    chain_name: Chains = Chains.TESTNET

    @property
    def infura_rpc_url(self):
        return INFURA_RPC_URLS[self.chain_name]


class EthereumVaults(BaseEnum):
    """All available Vaults enabled by Ribbon"""

    THETA_ETH_CALL = "RibbonThetaVaultETHCall"
    THETA_WBTC_CALL = "RibbonThetaVaultWBTCCall"
