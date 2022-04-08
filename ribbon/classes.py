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
from enum import Enum, EnumMeta


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
    """Bid parameters"""

    swapId: int
    nonce: int
    signerWallet: str
    sellAmount: int
    buyAmount: int
    referrer: str


@dataclass
class SignedBid(Bid):
    """Signed bid fields"""

    v: int
    r: str
    s: str


class MembershipTestEnumMeta(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BaseEnum(Enum, metaclass=MembershipTestEnumMeta):
    """With this you can do membership tests,
    e.g. >>> element in YourEnumClass"""


class Chains(BaseEnum):
    """Maybe to be called EtherumChains?
    Note: to test membership you can do
    >>> if my_current_chain in Chains.__members__
    """

    PROD = "mainnet"
    TESTNET = "kovan"


class InfuraAPIVersions(Enum):
    V3 = "v3"


INFURA_RPC_URLS = {
    Chains.PROD: f"https://mainnet.infura.io/{InfuraAPIVersions.V3.value}/",
    Chains.TESTNET: f"https://kovan.infura.io/{InfuraAPIVersions.V3.value}/",
}


@dataclass
class ContractConfig:
    """Configuration needed to connect to a Contract"""

    chain_name: Chains = Chains.TESTNET
    version: int = 1
    # salt: str = None

    @property
    def infura_rpc_url(self):
        return INFURA_RPC_URLS[self.chain_name]


@dataclass
class Vaults:
    """Vault representation"""

    address: str
    bidding_token: str


class EthereumVaults(BaseEnum):
    """All available Vaults enabled by Ribbon"""

    THETA_ETH_CALL = "RibbonThetaVaultETHCall"
    THETA_WBTC_CALL = "RibbonThetaVaultWBTCCall"
