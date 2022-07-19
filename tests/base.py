from importlib import import_module

import pytest

from opyn.chains import Chains as OpynChains
from ribbon.chains import Chains as RibbonChains

RIBBON = 'ribbon'
OPYN = 'opyn'
FRIKTION = 'friktion'
VENUES = [RIBBON, OPYN]
# DO NOT COMMIT!
VENUES = [RIBBON]

# DOV_VRFQ_RPC_TOKEN = os.environ["DOV_VRFQ_RPC_TOKEN"]

VENUE_CONFIGURATION = {
    RIBBON: {
        "chain_id": RibbonChains.KOVAN,
        # "rpc_uri": f"https://kovan.infura.io/v3/{DOV_VRFQ_RPC_TOKEN}",
    },
    OPYN: {
        "chain_id": OpynChains.ROPSTEN,
        # "rpc_uri": f"https://ropsten.infura.io/v3/{DOV_VRFQ_RPC_TOKEN}",
    },
    FRIKTION: {},
}
# https://web3js.readthedocs.io/en/v1.2.11/web3-utils.html
VALID_ADDRESS = "0xc1912fee45d61c87cc5ea59dae31190fffff232d"
PUBLIC_KEY = "0x0000000000000000000000000000000000000000"
PRIVATE_KEY = "0x0000000000000000000000000000000000000000000000000000000000000000"


class TestsBase:
    def setUp(self):
        pass

    @staticmethod
    def import_module(*args: str) -> str:
        return import_module(".".join(args))

    @pytest.fixture()
    def contract_config(self, venue):
        venue_config = VENUE_CONFIGURATION.get(venue, {})
        chain_id = venue_config.get("chain_id", 0)
        rpc_uri = venue_config.get("rpc_uri")

        module = self.import_module(venue, "definitions")
        ContractConfig = getattr(module, "ContractConfig")

        yield ContractConfig(address=VALID_ADDRESS, rpc_uri=rpc_uri, chain_id=chain_id)
