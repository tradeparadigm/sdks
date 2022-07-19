import pytest

from tests.base import PRIVATE_KEY, PUBLIC_KEY, VENUES, TestsBase

# from unittest.mock import patch


class TestWallet(TestsBase):
    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_wallet_module(self, venue):
        """equivalent to import venue.wallet"""
        self.import_module(venue, "wallet")

    @pytest.mark.parametrize("venue", VENUES)
    def test_can_import_wallet_class(self, venue):
        """equivalent to from venue.wallet import Wallet"""
        module = self.import_module(venue, "wallet")
        assert hasattr(module, "Wallet")

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
    def test_wallet_verify_allowance(self, venue, contract_config):
        """
        NOT IMPLEMENTED
        verify Wallet.verify_allowance
        """
        module = self.import_module(venue, "wallet")
        Wallet = getattr(module, "Wallet")

        assert Wallet is not None

    #     Wallet("0x...", None).verify_allowance(contract_config, VALID_ADDRESS)
