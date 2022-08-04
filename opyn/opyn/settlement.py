#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Haythem@Opyn, Anil@Opyn
# Created Date: 06/08/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module to call Swap contract """
# ---------------------------------------------------------------------------

from dataclasses import asdict
from shutil import ExecError
from typing import cast

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from web3 import Web3

from opyn.contract import ContractConnection
from opyn.definitions import BidData, Offer
from opyn.utils import ADDRESS_ZERO, get_address
from opyn.wallet import Wallet
from sdk_commons.config import OfferDetails


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
            offer (dict): Offer dictionary containing necessary
                parameters to create a new offer
            wallet (Wallet): Wallet class instance

        Raises:
            TypeError: Offer argument is not an Offer class instance
            ExecError: Transaction reverted

        Returns:
            offerId (int): OfferId of the created order
        """
        if not isinstance(offer, Offer):
            raise TypeError("Invalid offer")

        offer.offerToken = get_address(offer.offerToken)
        offer.bidToken = get_address(offer.bidToken)

        nonce = self.w3.eth.get_transaction_count(wallet.public_key)
        tx = self.contract.functions.createOffer(*list(asdict(offer).values())).buildTransaction(
            {
                "nonce": nonce,
                "gas": 3000000,
            }
        )

        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=wallet.private_key)

        self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        tx_receipt = self.w3.eth.wait_for_transaction_receipt(signed_tx.hash, timeout=600)

        if tx_receipt.status == 0:
            raise ExecError(f'Transaction reverted: {signed_tx.hash.hex()}')

        return cast(
            str,
            self.contract.events.CreateOffer().processReceipt(tx_receipt)[0]["args"]["offerId"],
        )

    def get_offer_details(self, offer_id: int) -> OfferDetails:
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
            'oToken': details[1],
            'biddingToken': details[2],
            'minPrice': details[3],
            'minBidSize': details[4],
            'totalSize': details[5],
            'availableSize': details[5],
        }

    def validate_bid(self, bid: BidData) -> str:
        """
        Method to validate bid

        Args:
            bid (dict): Bid dictionary containing offerId, bidId,
            signerAddress, bidderAddress, bidToken, offerToken,
            bidAmount, sellAmount, v, r, s

        Raises:
            TypeError: Bid argument is not an instance of SignedBid

        Returns:
            response (dict): Dictionary containing number of errors
            and the corresponding error messages
        """
        if not isinstance(bid, BidData):
            raise TypeError("Invalid signed bid")

        bid.signerAddress = get_address(bid.signerAddress)
        bid.bidderAddress = get_address(bid.bidderAddress)
        bid.bidToken = get_address(bid.bidToken)
        bid.offerToken = get_address(bid.offerToken)
        bid.v = bid.v + (bid.v < 27) * 27

        response = self.contract.functions.checkBid(asdict(bid)).call()

        errors = response[0]
        if errors == 0:
            return {"errors": 0}
        else:
            return {
                "errors": errors,
                "messages": [Web3.toText(msg).replace("\x00", "") for msg in response[1][:errors]],
            }

    def get_bid_signer(self, bid: BidData) -> str:
        if not isinstance(bid, BidData):
            raise TypeError("Invalid signed bid")

        signer_address = self.contract.functions.getBidSigner(asdict(bid)).call()

        return signer_address

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
