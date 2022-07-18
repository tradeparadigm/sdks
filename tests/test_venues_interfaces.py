import dataclasses
import os
from enum import Enum
from importlib import import_module

import pytest

from opyn.chains import Chains as OpynChains
from ribbon.chains import Chains as RibbonChains

# from unittest.mock import patch


RIBBON = 'ribbon'
OPYN = 'opyn'
FRIKTION = 'friktion'
VENUES = [RIBBON, OPYN]

DOV_VRFQ_RPC_TOKEN = os.environ["DOV_VRFQ_RPC_TOKEN"]

VENUE_CONFIGURATION = {
    RIBBON: {
        "chain_id": RibbonChains.KOVAN,
        "rpc_uri": f"https://kovan.infura.io/v3/{DOV_VRFQ_RPC_TOKEN}",
    },
    OPYN: {
        "chain_id": OpynChains.ROPSTEN,
        "rpc_uri": f"https://ropsten.infura.io/v3/{DOV_VRFQ_RPC_TOKEN}",
    },
    FRIKTION: {},
}
# https://web3js.readthedocs.io/en/v1.2.11/web3-utils.html
VALID_ADDRESS = "0xc1912fee45d61c87cc5ea59dae31190fffff232d"


def concat_module(*args: str) -> str:
    return ".".join(args)


@pytest.fixture()
def contract_config(venue):
    venue_config = VENUE_CONFIGURATION.get(venue, {})
    chain_id = venue_config.get("chain_id", 0)
    rpc_uri = venue_config.get("rpc_uri")

    module = import_module(concat_module(venue, "definitions"))
    ContractConfig = getattr(module, "ContractConfig")

    yield ContractConfig(address=VALID_ADDRESS, rpc_uri=rpc_uri, chain_id=chain_id)


@pytest.mark.parametrize("venue", VENUES)
def test_can_import_sdk_module(venue):
    """equivalent to import venue"""
    import_module(venue)


@pytest.mark.parametrize("venue", VENUES)
def test_can_import_chains_module(venue):
    """equivalent to import venue.chains"""
    import_module(concat_module(venue, "chains"))


@pytest.mark.parametrize("venue", VENUES)
def test_can_import_definitions_module(venue):
    """equivalent to import venue.definitions"""
    import_module(concat_module(venue, "definitions"))


@pytest.mark.parametrize("venue", VENUES)
def test_can_import_otoken_module(venue):
    """equivalent to import venue.otoken"""
    import_module(concat_module(venue, "otoken"))


@pytest.mark.parametrize("venue", VENUES)
def test_can_import_settlement_module(venue):
    """
    equivalent to import venue.settlement for Opyn
    equivalent to import venue.swap for others
    """
    if venue == OPYN:
        import_module(concat_module(venue, "settlement"))
    else:
        import_module(concat_module(venue, "swap"))


@pytest.mark.parametrize("venue", VENUES)
def test_can_import_wallet_module(venue):
    """equivalent to import venue.wallet"""
    import_module(concat_module(venue, "wallet"))


@pytest.mark.parametrize("venue", VENUES)
def test_can_import_chains_class(venue):
    """equivalent to from venue.chains import Chains"""
    module = import_module(concat_module(venue, "chains"))
    assert hasattr(module, "Chains")


@pytest.mark.parametrize("venue", VENUES)
def test_can_import_contract_config_class(venue):
    """equivalent to from venue.definitions import ContractConfig"""
    module = import_module(concat_module(venue, "definitions"))
    assert hasattr(module, "ContractConfig")


@pytest.mark.parametrize("venue", VENUES)
def test_can_import_bid_message_class(venue):
    """
    equivalent to from venue.definitions import MessageToSign for Opyn
    equivalent to from venue.definitions import SignedBid for others
    """
    module = import_module(concat_module(venue, "definitions"))

    if venue == OPYN:
        assert hasattr(module, "MessageToSign")
    else:
        assert hasattr(module, "SignedBid")


@pytest.mark.parametrize("venue", VENUES)
def test_can_import_otoken_class(venue):
    """equivalent to from venue.otoken import oTokenContract"""
    module = import_module(concat_module(venue, "otoken"))
    assert hasattr(module, "oTokenContract")


@pytest.mark.parametrize("venue", VENUES)
def test_can_import_swap_contract_class(venue):
    """
    equivalent to from venue.settlement import SettlementContract for Opyn
    equivalent to from venue.swap import SwapContract for others
    """
    if venue == OPYN:
        module = import_module(concat_module(venue, "settlement"))
        assert hasattr(module, "SettlementContract")
    else:
        module = import_module(concat_module(venue, "swap"))
        assert hasattr(module, "SwapContract")


@pytest.mark.parametrize("venue", VENUES)
def test_can_import_wallet_class(venue):
    """equivalent to from venue.wallet import Wallet"""
    module = import_module(concat_module(venue, "wallet"))
    assert hasattr(module, "Wallet")


@pytest.mark.parametrize("venue", VENUES)
def test_chains_class_is_enum(venue):
    """verify venue.chains.Chains"""
    module = import_module(concat_module(venue, "chains"))
    Chains = getattr(module, "Chains")

    assert Chains is not None
    assert issubclass(Chains, Enum)


@pytest.mark.parametrize("venue", VENUES)
def test_contract_config_is_dataclass(venue):
    """verify venue.chains.ContractConfig"""
    module = import_module(concat_module(venue, "definitions"))
    ContractConfig = getattr(module, "ContractConfig")

    assert ContractConfig is not None
    dataclasses.is_dataclass(ContractConfig)


@pytest.mark.parametrize("venue", VENUES)
def test_contract_config_attributes(venue):
    """verify venue.chains.ContractConfig"""
    module = import_module(concat_module(venue, "definitions"))
    ContractConfig = getattr(module, "ContractConfig")

    class_fields = {f.name: f for f in dataclasses.fields(ContractConfig)}
    assert "address" in class_fields
    assert "rpc_uri" in class_fields
    assert "chain_id" in class_fields

    module = import_module(concat_module(venue, "chains"))
    Chains = getattr(module, "Chains")

    assert issubclass(class_fields['address'].type, str)
    assert issubclass(class_fields['rpc_uri'].type, str)
    assert issubclass(class_fields['chain_id'].type, Chains)


@pytest.mark.parametrize("venue", VENUES)
def test_bid_message_is_dataclass(venue):
    """verify venue.chains.MessageToSign"""

    module = import_module(concat_module(venue, "definitions"))

    if venue == OPYN:
        SignedBid = getattr(module, "MessageToSign")
    else:
        SignedBid = getattr(module, "SignedBid")

    assert SignedBid is not None
    dataclasses.is_dataclass(SignedBid)


@pytest.mark.parametrize("venue", VENUES)
def test_bid_message_attributes(venue):
    """verify venue.chains.MessageToSign"""

    module = import_module(concat_module(venue, "definitions"))

    if venue == OPYN:
        SignedBid = getattr(module, "MessageToSign")
    else:
        SignedBid = getattr(module, "SignedBid")

    class_fields = {f.name: f for f in dataclasses.fields(SignedBid)}
    assert "swapId" in class_fields
    assert "nonce" in class_fields
    assert "signerWallet" in class_fields
    assert "sellAmount" in class_fields
    assert "buyAmount" in class_fields
    assert "referrer" in class_fields
    assert "v" in class_fields
    assert "r" in class_fields
    assert "s" in class_fields

    assert issubclass(class_fields['swapId'].type, int)
    assert issubclass(class_fields['nonce'].type, int)
    assert issubclass(class_fields['signerWallet'].type, str)
    assert issubclass(class_fields['sellAmount'].type, int)
    assert issubclass(class_fields['buyAmount'].type, int)
    assert issubclass(class_fields['referrer'].type, str)
    assert issubclass(class_fields['v'].type, int)
    assert issubclass(class_fields['r'].type, str)
    assert issubclass(class_fields['s'].type, str)


@pytest.mark.parametrize("venue", VENUES)
def test_otoken_class(venue):
    """verify venue.otoken.oTokenContract"""
    module = import_module(concat_module(venue, "otoken"))

    oTokenContract = getattr(module, "oTokenContract")

    assert oTokenContract is not None
    assert isinstance(oTokenContract, type)

    assert hasattr(oTokenContract, "get_otoken_details")


@pytest.mark.parametrize("venue", VENUES)
def test_swap_contract_class(venue):
    """
    verify venue.settlement.SettlementContract for Opyn
    verify venue.swap.SwapContract for others
    """

    if venue == OPYN:
        module = import_module(concat_module(venue, "settlement"))
        SwapContract = getattr(module, "SettlementContract")
    else:
        module = import_module(concat_module(venue, "swap"))
        SwapContract = getattr(module, "SwapContract")

    assert SwapContract is not None

    assert hasattr(SwapContract, "get_offer_details")
    assert hasattr(SwapContract, "validate_bid")
    assert hasattr(SwapContract, "create_offer")


@pytest.mark.parametrize("venue", VENUES)
def test_wallet_class(venue):
    """verify venue.wallet.Wallet"""
    module = import_module(concat_module(venue, "wallet"))
    Wallet = getattr(module, "Wallet")

    assert Wallet is not None

    # sign_bid from Ribbon not used by APIs
    # sign_bid_data from Opyn not used by APIs
    # allow_more from Opyn not used by APIs
    assert hasattr(Wallet, "verify_allowance")


# @pytest.mark.parametrize("venue", VENUES)
# def test_otoken_get_otoken_details(venue, contract_config):
#     """
#       NOT IMPLEMENTED
#       verify oTokenContract.get_otoken_details
#     """
#     module = import_module(concat_module(venue, "otoken"))
#     oTokenContract = getattr(module, "oTokenContract")

#     class_instance = oTokenContract(contract_config)

#     with patch(f"{venue}.otoken.oTokenContract") as mocked_oTokenContract:
#         mocked_oTokenContract.contract.functions.getOtokenDetails.return_value = [
#             "a", "b", "c", "d", "e", "f"
#         ]
#         details = class_instance.get_otoken_details()

#     assert details ...


# @pytest.mark.parametrize("venue", VENUES)
# def test_swap_contract_get_offer_details(venue, contract_config):
#     """
#       NOT IMPLEMENTED
#       verify SwapContract.get_offer_details
#     """

#     if venue == OPYN:
#         module = import_module(concat_module(venue, "settlement"))
#         SwapContract = getattr(module, "SettlementContract")
#     else:
#         module = import_module(concat_module(venue, "swap"))
#         SwapContract = getattr(module, "SwapContract")

#     assert SwapContract is not None

#     SwapContract(contract_config).get_offer_details(1)


# @pytest.mark.parametrize("venue", VENUES)
# def test_swap_contract_validate_bid(venue, contract_config):
#     """
#       NOT IMPLEMENTED
#       verify SwapContract.validate_bid
#     """

#     if venue == OPYN:
#         module = import_module(concat_module(venue, "settlement"))
#         SwapContract = getattr(module, "SettlementContract")
#     else:
#         module = import_module(concat_module(venue, "swap"))
#         SwapContract = getattr(module, "SwapContract")

#     assert SwapContract is not None

#     SwapContract(contract_config).validate_bid()


# @pytest.mark.parametrize("venue", VENUES)
# def test_swap_contract_create_offer(venue, contract_config):
#     """
#       NOT IMPLEMENTED
#       verify SwapContract.create_offer
#     """

#     if venue == OPYN:
#         module = import_module(concat_module(venue, "settlement"))
#         SwapContract = getattr(module, "SettlementContract")
#     else:
#         module = import_module(concat_module(venue, "swap"))
#         SwapContract = getattr(module, "SwapContract")

#     assert SwapContract is not None

#     SwapContract(contract_config).create_offer()


# @pytest.mark.parametrize("venue", VENUES)
# def test_wallet_verify_allowance(venue, contract_config):
#     """
#       NOT IMPLEMENTED
#       verify Wallet.verify_allowance
#     """
#     module = import_module(concat_module(venue, "wallet"))
#     Wallet = getattr(module, "Wallet")

#     assert Wallet is not None

#     Wallet("0x...", None).verify_allowance(contract_config, VALID_ADDRESS)
