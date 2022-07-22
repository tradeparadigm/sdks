#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Steven@Ribbon, Paolo@Paradigm
# Created Date: 04/04/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module to store data classes """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from dataclasses import dataclass

from ribbon.chains import Chains
from ribbon.encode import ADDRESS_ZERO


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------
@dataclass
class Domain:
    """
    Domain parameters for signatures

    TODO: see if you can leverage this ID
    to know which chain we are using
    maybe to do in the smart contract itself
    https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.chain_id
    """

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
    referrer: str = ADDRESS_ZERO


@dataclass
class SignedBid(Bid):
    v: int = None
    r: str = None
    s: str = None


@dataclass
class Offer:
    oToken: str
    biddingToken: str
    minPrice: int
    minBidSize: int
    offerAmount: int


@dataclass
class ContractConfig:
    """Configuration needed to connect to a Contract"""

    address: str
    rpc_uri: str
    chain_id: Chains = Chains.ETHEREUM
