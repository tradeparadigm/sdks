""" Module to store data classes """
from dataclasses import dataclass
from typing import Optional

from sdk_commons.chains import Chains


@dataclass
class Bid:
    vaultAddress: str
    nonce: int
    signerWallet: str
    sellAmount: int
    buyAmount: int
    referrer: str
