#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# Created By: Steven@Ribbon, Paolo@Paradigm
# Created Date: 04/04/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module to call oToken contract """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from ribbon.erc20 import ERC20Contract
from sdk_commons.config import OfferTokenDetails
from sdk_commons.helpers import get_abi_path


# ---------------------------------------------------------------------------
# oToken Contract
# ---------------------------------------------------------------------------
class oTokenContract(ERC20Contract):
    """
    Object to create connection to the an oToken contract

    Args:
        config (ContractConfig): Configuration to setup the Contract
    """

    abi_location = get_abi_path('Ribbon_oToken')

    def get_otoken_details(self) -> OfferTokenDetails:
        """
        Method to validate bid

        Args:

        Returns:
            response (dict): Dictionary oToken details
        """
        details = self.contract.functions.getOtokenDetails().call()

        return {
            "collateralAsset": details[0],
            "underlyingAsset": details[1],
            "strikeAsset": details[2],
            "strikePrice": details[3],
            "expiryTimestamp": details[4],
            "isPut": details[5],
        }
