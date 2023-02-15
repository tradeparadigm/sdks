""" Module to store data classes """
from dataclasses import dataclass


@dataclass
class Bid:
    vaultAddress: str
    nonce: int
    signerWallet: str
    sellAmount: int
    buyAmount: int
    referrer: str
