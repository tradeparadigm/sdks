from importlib import import_module
from test.base import VENUES, TestsBase

import pytest


class TestSDK(TestsBase):
    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_sdk_module(self, venue):
        """equivalent to import venue"""
        import_module(venue)
