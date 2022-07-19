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
        self.import_class(venue, "definitions", "ContractConfig")

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_domain_class(self, venue):
        """equivalent to from venue.definitions import Domain"""
        self.import_class(venue, "definitions", "Domain")

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_bid_message_class(self, venue):
        """
        equivalent to from venue.definitions import MessageToSign for Opyn
        equivalent to from venue.definitions import SignedBid for others
        """

        if venue == OPYN:
            self.import_class(venue, "definitions", "MessageToSign")
        else:
            self.import_class(venue, "definitions", "SignedBid")

    @pytest.mark.parametrize("venue", VENUES)
    def test_domain_is_dataclass(self, venue):
        """verify venue.chains.Domain"""
        Domain = self.import_class(venue, "definitions", "Domain")
        dataclasses.is_dataclass(Domain)

    @pytest.mark.parametrize("venue", VENUES)
    def test_domain_attributes(self, venue):
        """verify venue.chains.Domain"""
        Domain = self.import_class(venue, "definitions", "Domain")

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
        ContractConfig = self.import_class(venue, "definitions", "ContractConfig")
        dataclasses.is_dataclass(ContractConfig)

    @pytest.mark.parametrize("venue", VENUES)
    def test_contract_config_attributes(self, venue):
        """verify venue.chains.ContractConfig"""
        ContractConfig = self.import_class(venue, "definitions", "ContractConfig")

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

        if venue == OPYN:
            SignedBid = self.import_class(venue, "definitions", "MessageToSign")
        else:
            SignedBid = self.import_class(venue, "definitions", "SignedBid")

        dataclasses.is_dataclass(SignedBid)

    @pytest.mark.parametrize("venue", VENUES)
    def test_bid_message_attributes(self, venue):
        """verify venue.chains.MessageToSign"""

        if venue == OPYN:
            SignedBid = self.import_class(venue, "definitions", "MessageToSign")
        else:
            SignedBid = self.import_class(venue, "definitions", "SignedBid")

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
