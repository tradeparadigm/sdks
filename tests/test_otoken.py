import pytest

from tests.base import VENUES, TestsBase

# from unittest.mock import patch


class TestOToken(TestsBase):
    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_otoken_module(self, venue):
        """equivalent to import venue.otoken"""
        self.import_module(venue, "otoken")

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_otoken_class(self, venue):
        """equivalent to from venue.otoken import oTokenContract"""
        self.import_class(venue, "otoken", "oTokenContract")

    @pytest.mark.parametrize("venue", VENUES)
    def test_otoken_class(self, venue):
        """verify venue.otoken.oTokenContract"""
        oTokenContract = self.import_class(venue, "otoken", "oTokenContract")

        assert isinstance(oTokenContract, type)

        assert hasattr(oTokenContract, "get_otoken_details")

    @pytest.mark.parametrize("venue", VENUES)
    def test_otoken_get_otoken_details(self, venue, contract_config):
        """
        NOT IMPLEMENTED
        verify oTokenContract.get_otoken_details
        """
        oTokenContract = self.import_class(venue, "otoken", "oTokenContract")

        print(oTokenContract)

    #     class_instance = oTokenContract(contract_config)

    #     with patch(f"{venue}.otoken.oTokenContract") as mocked_oTokenContract:
    #         mocked_oTokenContract.contract.functions.getOtokenDetails.return_value = [
    #             "a", "b", "c", "d", "e", "f"
    #         ]
    #         details = class_instance.get_otoken_details()

    #     assert details ...
