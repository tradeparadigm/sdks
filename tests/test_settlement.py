import pytest

from tests.base import OPYN, VENUES, TestsBase


class TestSettlement(TestsBase):
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
