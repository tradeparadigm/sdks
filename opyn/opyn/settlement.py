#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Steven@Ribbon, Paolo@Paradigm
# Created Date: 04/04/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module to call Swap contract """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from web3 import Web3
from dataclasses import asdict

from opyn.contract import ContractConnection
from opyn.wallet import Wallet
from opyn.utils import get_address
from opyn.definitions import OrderData


# ---------------------------------------------------------------------------
# Settlement Contract
# ---------------------------------------------------------------------------
class Settlement(ContractConnection):
    """
    Object to create connection to the Settlement contract

    Args:
        config (ContractConfig): Configuration to setup the Contract
    """

    def settleRfq(self, _offerOrder: OrderData, _bidOrder: OrderData):
        """
        Method to settle RFQ on chain

        Args:
            _offerOrder (OrderData): The offer related order data
            _bidOrder   (OrderData): The bid related order data

        Raises:
            ValueError: The argument is not a valid offer

        """

        self.contract.functions.settleRfq(_offerOrder, _bidOrder).call()

    def nonce(self, owner: str) -> int:
        """
        Method to get nonces

        Args:
            owner (str): The owner for which nonces is extracted

        Raises:
            ValueError: The argument is not a valid offer

        Returns:
            nonce (int): Nonce
        """
        nonces = self.contract.functions.nonces(owner).call()

        return nonces

    def domainSeparator(self) -> str:
        domain = self.contract.functions.DOMAIN_SEPARATOR().call()

        return domain
