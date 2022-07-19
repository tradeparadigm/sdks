import dataclasses

import pytest

from tests.base import OPYN, VENUES, TestsBase


class TestDefinitions(TestsBase):
    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_definitions_module(self, venue):
        """equivalent to import venue.definitions"""
        self.import_module(venue, "definitions")

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
