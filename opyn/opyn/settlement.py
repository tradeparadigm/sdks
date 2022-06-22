#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Haythem@Opyn, Anil@Opyn
# Created Date: 06/08/2022
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
from opyn.definitions import Offer
from opyn.wallet import Wallet

# ---------------------------------------------------------------------------
# Settlement Contract
# ---------------------------------------------------------------------------
class SettlementContract(ContractConnection):
    """
    Object to create connection to the Settlement contract

    Args:
        config (ContractConfig): Configuration to setup the Contract
    """

    def create_offer(self, offer: Offer, wallet: Wallet) -> str:
        """
        Method to create offer

        Args:
            offer (dict): Offer dictionary containing necessary parameters 
                to create a new offer
            wallet (Wallet): Wallet class instance

        Raises:
            TypeError: Offer argument is not a valid instance of Offer class
            ExecError: Transaction reverted

        Returns:
            offerId (int): OfferId of the created order
        """
        if not isinstance(offer, Offer):
            raise TypeError("Invalid offer")

        offer.offerToken = get_address(offer.offerToken)
        offer.bidToken = get_address(offer.bidToken)

        nonce = self.w3.eth.get_transaction_count(wallet.public_key) 
        tx = self.contract.functions.createOffer(*list(asdict(offer).values())) \
            .buildTransaction({
                "nonce": nonce,
                "gas": 150000,
            })

        signed_tx = self.w3.eth.account \
            .sign_transaction(tx, private_key=wallet.private_key)

        self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        tx_receipt = self.w3.eth \
            .wait_for_transaction_receipt(signed_tx.hash, timeout=600)
        
        if tx_receipt.status == 0:
            raise ExecError(f'Transaction reverted: {signed_tx.hash.hex()}')
        else:
            return self.contract.events.CreateOffer() \
                .processReceipt(tx_receipt)[0]["args"]["offerId"]


    def get_offer_details(self, offer_id: int) -> dict:
        """
        Method to get bid details

        Args:
            offer_id (int): Offer ID

        Raises:
            ValueError: The argument is not a valid offer

        Returns:
            details (dict): Offer details
        """
        details = self.contract.functions.getOfferDetails(offer_id).call()
        seller = details[0]

        if seller == ADDRESS_ZERO:
            raise ValueError(f'Offer does not exist: {offer_id}')

        return {
            'seller': details[0],
            'offerToken': details[1],
            'bidToken': details[3],
            'minPrice': details[2],
            'minBidSize': details[4]
        }

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

    def get_offer_counter(self) -> int:
        """
        Method to get offersCounter

        Returns:
            counter (int): Number of created offers
        """
        counter = self.contract.functions.offersCounter().call()

        return counter
