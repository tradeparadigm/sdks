from enum import Enum
from meta import BaseEnum


class Chains(BaseEnum):
    PROD = "mainnet"
    TESTNET = "kovan"


class InfuraAPIVersions(Enum):
    V3 = "v3"


INFURA_RPC_URLS = {
    Chains.PROD: f"https://mainnet.infura.io/{InfuraAPIVersions.V3.value}/",
    Chains.TESTNET: f"https://kovan.infura.io/{InfuraAPIVersions.V3.value}/",
}
