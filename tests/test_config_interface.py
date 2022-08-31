import pytest

from sdk_commons.chains import Chains
from sdk_commons.config import SDKConfig
from tests.base import VENUES, TestsBase

ADDRESS_ZERO = "0x0000000000000000000000000000000000000000"


class TestConfig(TestsBase):
    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_config_module(self, venue: str):
        """Verify if venue.config can be imported"""
        self.import_module(venue, "config")

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_config_class(self, venue: str):
        """Verify that venue.config contains a config class"""

        config_class = self.get_config_class(venue)

        self.import_class(venue, "config", config_class)

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_instantiate_config_class(self, venue: str):
        """
        Verify that the config class instantiated.
        This test can fail if the config class does not
        correctly implement all abstract methods
        """

        config_class = self.import_class(venue, "config", self.get_config_class(venue))
        config_class()

    @pytest.mark.parametrize("venue", VENUES)
    def test_create_offer_signature(self, venue: str):
        """Verify the signature of create_offer"""

        config_class_name = self.get_config_class(venue)
        config_class = self.import_class(venue, "config", config_class_name)
        c = config_class()

        self.inspect_method_signature(
            c.create_offer,
            reference=SDKConfig.create_offer,
        )

    @pytest.mark.parametrize("venue", VENUES)
    def test_get_otoken_details_signature(self, venue: str):
        """Verify the signature of get_otoken_details"""

        config_class_name = self.get_config_class(venue)
        config_class = self.import_class(venue, "config", config_class_name)
        c = config_class()

        self.inspect_method_signature(
            c.get_otoken_details,
            reference=SDKConfig.get_otoken_details,
        )

    @pytest.mark.parametrize("venue", VENUES)
    def test_get_offer_details_signature(self, venue: str):
        """Verify the signature of get_offer_details"""

        config_class_name = self.get_config_class(venue)
        config_class = self.import_class(venue, "config", config_class_name)
        c = config_class()

        self.inspect_method_signature(
            c.get_offer_details,
            reference=SDKConfig.get_offer_details,
        )

    @pytest.mark.parametrize("venue", VENUES)
    def test_sign_bid_signature(self, venue: str):
        """Verify the signature of sign_bid"""

        config_class_name = self.get_config_class(venue)
        config_class = self.import_class(venue, "config", config_class_name)
        c = config_class()

        self.inspect_method_signature(
            c.sign_bid,
            reference=SDKConfig.sign_bid,
        )

    @pytest.mark.parametrize("venue", VENUES)
    def test_validate_bid_signature(self, venue: str):
        """Verify the signature of validate_bid"""

        config_class_name = self.get_config_class(venue)
        config_class = self.import_class(venue, "config", config_class_name)
        c = config_class()

        self.inspect_method_signature(
            c.validate_bid,
            reference=SDKConfig.validate_bid,
        )

    @pytest.mark.parametrize("venue", VENUES)
    def test_verify_allowance_signature(self, venue: str):
        """Verify the signature of verify_allowance"""

        config_class_name = self.get_config_class(venue)
        config_class = self.import_class(venue, "config", config_class_name)
        c = config_class()

        self.inspect_method_signature(
            c.verify_allowance,
            reference=SDKConfig.verify_allowance,
        )

    @pytest.mark.parametrize("venue", VENUES)
    def test_config_class_has_supported_chains(self, venue: str):
        """Verify config class has supported_chains list"""

        config_class = self.import_class(venue, "config", self.get_config_class(venue))
        assert hasattr(config_class, "supported_chains")

        supported_chains = getattr(config_class, "supported_chains")

        assert isinstance(supported_chains, list), "supported_chains is not a list"

        for chain in supported_chains:
            assert isinstance(chain, Chains)

    @pytest.mark.parametrize("venue", VENUES)
    def test_config_class_has_authorization_pages(self, venue: str):
        """
        Verify config class has authorization_pages
        and also verify that the authorization pages contains
        expended mainnet and testnet fields
        """

        config_class = self.import_class(venue, "config", self.get_config_class(venue))
        assert hasattr(config_class, "authorization_pages")

        authorization_pages = getattr(config_class, "authorization_pages")()

        assert hasattr(
            authorization_pages, "mainnet"
        ), f"mainnet not found in {authorization_pages}"

        assert hasattr(
            authorization_pages, "testnet"
        ), f"testnet not found in {authorization_pages}"
