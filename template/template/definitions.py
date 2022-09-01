""" Module to store data classes """
from dataclasses import dataclass
from typing import Optional

from sdk_commons.chains import Chains


@dataclass
class Bid:
    swapId: int
    nonce: int
    signerWallet: str
    sellAmount: int
    buyAmount: int
    referrer: str


@dataclass
class Domain:
    """
    Domain parameters for signatures
    """

    name: str
    version: str
    chainId: int
    verifyingContract: str


@dataclass
class ContractConfig:
    """Configuration needed to connect to a Contract"""

    address: str
    rpc_uri: str
    chain_id: Chains


@dataclass
class Offer:
    oToken: str
    biddingToken: str
    minPrice: int
    minBidSize: int
    offerAmount: int


@dataclass
class SignedBid:
    swapId: int
    nonce: int
    signerWallet: str
    sellAmount: int
    buyAmount: int
    referrer: str
    v: Optional[int] = None
    r: Optional[str] = None
    s: Optional[str] = None
