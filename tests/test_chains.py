from enum import Enum

import pytest

from tests.base import VENUES, TestsBase


class TestChains(TestsBase):
    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_chains_module(self, venue):
        """equivalent to import venue.chains"""
        self.import_module(venue, "chains")

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_chains_class(self, venue):
        """equivalent to from venue.chains import Chains"""
        self.import_class(venue, "chains", "Chains")

    @pytest.mark.parametrize("venue", VENUES)
    def test_chains_class_is_enum(self, venue):
        """verify venue.chains.Chains"""
        Chains = self.import_class(venue, "chains", "Chains")
        assert issubclass(Chains, Enum)
