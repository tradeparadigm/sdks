#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Anil@Opyn
# Created Date: 06/08/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module to call oToken contract """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from opyn.erc20 import ERC20Contract


# ---------------------------------------------------------------------------
# oToken Contract
# ---------------------------------------------------------------------------
class oTokenContract(ERC20Contract):
    """
    Object to create connection to the an oToken contract

    Args:
        config (ContractConfig): Configuration to setup the Contract
    """

    abi_location = 'abis/oToken.json'

    def get_otoken_details(self) -> dict:
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
