import dataclasses
from enum import Enum
from importlib import import_module

import pytest

from tests.base import OPYN, PRIVATE_KEY, PUBLIC_KEY, VENUES, TestsBase

# from unittest.mock import patch


class TestVenues(TestsBase):
    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_sdk_module(self, venue):
        """equivalent to import venue"""
        import_module(venue)

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_chains_module(self, venue):
        """equivalent to import venue.chains"""
        self.import_module(venue, "chains")

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_definitions_module(self, venue):
        """equivalent to import venue.definitions"""
        self.import_module(venue, "definitions")

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_otoken_module(self, venue):
        """equivalent to import venue.otoken"""
        self.import_module(venue, "otoken")

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_settlement_module(self, venue):
        """
        equivalent to import venue.settlement for Opyn
        equivalent to import venue.swap for others
        """
        if venue == OPYN:
            self.import_module(venue, "settlement")
        else:
            self.import_module(venue, "swap")

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_wallet_module(self, venue):
        """equivalent to import venue.wallet"""
        self.import_module(venue, "wallet")

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_chains_class(self, venue):
        """equivalent to from venue.chains import Chains"""
        module = self.import_module(venue, "chains")
        assert hasattr(module, "Chains")

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_contract_config_class(self, venue):
        """equivalent to from venue.definitions import ContractConfig"""
        module = self.import_module(venue, "definitions")
        assert hasattr(module, "ContractConfig")

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_domain_class(self, venue):
        """equivalent to from venue.definitions import Domain"""
        module = self.import_module(venue, "definitions")
        assert hasattr(module, "Domain")

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_bid_message_class(self, venue):
        """
        equivalent to from venue.definitions import MessageToSign for Opyn
        equivalent to from venue.definitions import SignedBid for others
        """
        module = self.import_module(venue, "definitions")

        if venue == OPYN:
            assert hasattr(module, "MessageToSign")
        else:
            assert hasattr(module, "SignedBid")

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_otoken_class(self, venue):
        """equivalent to from venue.otoken import oTokenContract"""
        module = self.import_module(venue, "otoken")
        assert hasattr(module, "oTokenContract")

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_swap_contract_class(self, venue):
        """
        equivalent to from venue.settlement import SettlementContract for Opyn
        equivalent to from venue.swap import SwapContract for others
        """
        if venue == OPYN:
            module = self.import_module(venue, "settlement")
            assert hasattr(module, "SettlementContract")
        else:
            module = self.import_module(venue, "swap")
            assert hasattr(module, "SwapContract")

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_wallet_class(self, venue):
        """equivalent to from venue.wallet import Wallet"""
        module = self.import_module(venue, "wallet")
        assert hasattr(module, "Wallet")

    @pytest.mark.parametrize("venue", VENUES)
    def test_chains_class_is_enum(self, venue):
        """verify venue.chains.Chains"""
        module = self.import_module(venue, "chains")
        Chains = getattr(module, "Chains")

        assert Chains is not None
        assert issubclass(Chains, Enum)

    @pytest.mark.parametrize("venue", VENUES)
    def test_domain_is_dataclass(self, venue):
        """verify venue.chains.Domain"""
        module = self.import_module(venue, "definitions")
        Domain = getattr(module, "Domain")

        assert Domain is not None
        dataclasses.is_dataclass(Domain)

    @pytest.mark.parametrize("venue", VENUES)
    def test_domain_attributes(self, venue):
        """verify venue.chains.Domain"""
        module = self.import_module(venue, "definitions")
        Domain = getattr(module, "Domain")

        class_fields = {f.name: f for f in dataclasses.fields(Domain)}
        assert "name" in class_fields
        assert "chainId" in class_fields
        assert "verifyingContract" in class_fields
        assert "version" in class_fields

        assert issubclass(class_fields['name'].type, str)
        assert issubclass(class_fields['chainId'].type, int)
        assert issubclass(class_fields['verifyingContract'].type, str)
        assert issubclass(class_fields['version'].type, int)

    @pytest.mark.parametrize("venue", VENUES)
    def test_contract_config_is_dataclass(self, venue):
        """verify venue.chains.ContractConfig"""
        module = self.import_module(venue, "definitions")
        ContractConfig = getattr(module, "ContractConfig")

        assert ContractConfig is not None
        dataclasses.is_dataclass(ContractConfig)

    @pytest.mark.parametrize("venue", VENUES)
    def test_contract_config_attributes(self, venue):
        """verify venue.chains.ContractConfig"""
        module = self.import_module(venue, "definitions")
        ContractConfig = getattr(module, "ContractConfig")

        class_fields = {f.name: f for f in dataclasses.fields(ContractConfig)}
        assert "address" in class_fields
        assert "rpc_uri" in class_fields
        assert "chain_id" in class_fields

        module = self.import_module(venue, "chains")
        Chains = getattr(module, "Chains")

        assert issubclass(class_fields['address'].type, str)
        assert issubclass(class_fields['rpc_uri'].type, str)
        assert issubclass(class_fields['chain_id'].type, Chains)

    @pytest.mark.parametrize("venue", VENUES)
    def test_bid_message_is_dataclass(self, venue):
        """verify venue.chains.MessageToSign"""

        module = self.import_module(venue, "definitions")

        if venue == OPYN:
            SignedBid = getattr(module, "MessageToSign")
        else:
            SignedBid = getattr(module, "SignedBid")

        assert SignedBid is not None
        dataclasses.is_dataclass(SignedBid)

    @pytest.mark.parametrize("venue", VENUES)
    def test_bid_message_attributes(self, venue):
        """verify venue.chains.MessageToSign"""

        module = self.import_module(venue, "definitions")

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
    def test_otoken_class(self, venue):
        """verify venue.otoken.oTokenContract"""
        module = self.import_module(venue, "otoken")

        oTokenContract = getattr(module, "oTokenContract")

        assert oTokenContract is not None
        assert isinstance(oTokenContract, type)

        assert hasattr(oTokenContract, "get_otoken_details")

    @pytest.mark.parametrize("venue", VENUES)
    def test_swap_contract_class(self, venue):
        """
        verify venue.settlement.SettlementContract for Opyn
        verify venue.swap.SwapContract for others
        """

        if venue == OPYN:
            module = self.import_module(venue, "settlement")
            SwapContract = getattr(module, "SettlementContract")
        else:
            module = self.import_module(venue, "swap")
            SwapContract = getattr(module, "SwapContract")

        assert SwapContract is not None

        assert hasattr(SwapContract, "get_offer_details")
        assert hasattr(SwapContract, "validate_bid")
        assert hasattr(SwapContract, "create_offer")

    @pytest.mark.parametrize("venue", VENUES)
    def test_wallet_class(self, venue):
        """verify venue.wallet.Wallet"""
        module = self.import_module(venue, "wallet")
        Wallet = getattr(module, "Wallet")

        assert Wallet is not None

        # sign_bid from Ribbon not used by APIs
        # sign_bid_data from Opyn not used by APIs
        # allow_more from Opyn not used by APIs
        assert hasattr(Wallet, "verify_allowance")

        assert Wallet(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)
        assert Wallet(public_key=PUBLIC_KEY, private_key=None)
        assert Wallet(public_key=None, private_key=PRIVATE_KEY)
        assert Wallet(public_key=PUBLIC_KEY)
        assert Wallet(private_key=PRIVATE_KEY)
        with pytest.raises(ValueError):
            assert Wallet()

    @pytest.mark.parametrize("venue", VENUES)
    def test_otoken_get_otoken_details(self, venue, contract_config):
        """
        NOT IMPLEMENTED
        verify oTokenContract.get_otoken_details
        """
        module = self.import_module(venue, "otoken")
        oTokenContract = getattr(module, "oTokenContract")

        print(oTokenContract)

    #     class_instance = oTokenContract(contract_config)

    #     with patch(f"{venue}.otoken.oTokenContract") as mocked_oTokenContract:
    #         mocked_oTokenContract.contract.functions.getOtokenDetails.return_value = [
    #             "a", "b", "c", "d", "e", "f"
    #         ]
    #         details = class_instance.get_otoken_details()

    #     assert details ...

    @pytest.mark.parametrize("venue", VENUES)
    def test_swap_contract_get_offer_details(self, venue, contract_config):
        """
        NOT IMPLEMENTED
        verify SwapContract.get_offer_details
        """

        if venue == OPYN:
            module = self.import_module(venue, "settlement")
            SwapContract = getattr(module, "SettlementContract")
        else:
            module = self.import_module(venue, "swap")
            SwapContract = getattr(module, "SwapContract")

        assert SwapContract is not None

    #     SwapContract(contract_config).get_offer_details(1)

    @pytest.mark.parametrize("venue", VENUES)
    def test_swap_contract_validate_bid(self, venue, contract_config):
        """
        NOT IMPLEMENTED
        verify SwapContract.validate_bid
        """

        if venue == OPYN:
            module = self.import_module(venue, "settlement")
            SwapContract = getattr(module, "SettlementContract")
        else:
            module = self.import_module(venue, "swap")
            SwapContract = getattr(module, "SwapContract")

        assert SwapContract is not None

    #     SwapContract(contract_config).validate_bid()

    @pytest.mark.parametrize("venue", VENUES)
    def test_swap_contract_create_offer(self, venue, contract_config):
        """
        NOT IMPLEMENTED
        verify SwapContract.create_offer
        """

        if venue == OPYN:
            module = self.import_module(venue, "settlement")
            SwapContract = getattr(module, "SettlementContract")
        else:
            module = self.import_module(venue, "swap")
            SwapContract = getattr(module, "SwapContract")

        assert SwapContract is not None

    #     SwapContract(contract_config).create_offer()

    @pytest.mark.parametrize("venue", VENUES)
    def test_wallet_verify_allowance(self, venue, contract_config):
        """
        NOT IMPLEMENTED
        verify Wallet.verify_allowance
        """
        module = self.import_module(venue, "wallet")
        Wallet = getattr(module, "Wallet")

        assert Wallet is not None

    #     Wallet("0x...", None).verify_allowance(contract_config, VALID_ADDRESS)
