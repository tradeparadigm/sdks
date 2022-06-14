#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Haythem@Opyn, Anil@Opyn
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
from opyn.utils import get_address
from opyn.definitions import OrderData

# ---------------------------------------------------------------------------
# Settlement Contract
# ---------------------------------------------------------------------------
class SettlementContract(ContractConnection):
    """
    Object to create connection to the Settlement contract

    Args:
        config (ContractConfig): Configuration to setup the Contract
    """

    def settleRfq(self, publicKey: str, privateKey: str, _offerOrder: OrderData, _bidOrder: OrderData):
        """
        Method to settle RFQ on chain

        Args:
            _offerOrder (OrderData): The offer related order data
            _bidOrder   (OrderData): The bid related order data

        Raises:
            ValueError: The argument is not a valid offer

        """
        if not isinstance(_offerOrder, OrderData):
            raise TypeError("Invalid offer order")

        if not isinstance(_bidOrder, OrderData):
            raise TypeError("Invalid bid order")
        
        nonce = self.w3.eth.get_transaction_count(publicKey) 
        tx = self.contract.functions.settleRfq(tuple(asdict(_offerOrder)), tuple(asdict(_offerOrder))) \
            .buildTransaction({
                "nonce": nonce
            })

        signed_tx = self.w3.eth.account \
            .sign_transaction(tx, private_key=privateKey)

        self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        tx_receipt = self.w3.eth \
            .wait_for_transaction_receipt(signed_tx.hash, timeout=600)

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
