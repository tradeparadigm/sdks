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
    chainId: int
    verifyingContract: str
    version: int
    salt: str = None


@dataclass
class Bid:
    buyAmount: int
    nonce: int
    sellAmount: int
    signerWallet: str
    swapId: int
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
    rpc_uri: str
    chain_name: str
