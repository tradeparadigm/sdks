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

from ribbon.contract import ContractConnection
from ribbon.definitions import SignedBid, Offer
from ribbon.wallet import Wallet
from ribbon.utils import get_address
from ribbon.encode import ADDRESS_ZERO
from shutil import ExecError


# ---------------------------------------------------------------------------
# Swap Contract
# ---------------------------------------------------------------------------
class SwapContract(ContractConnection):
    """
    Object to create connection to the Swap contract

    Args:
        config (ContractConfig): Configuration to setup the Contract
    """

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
        details = self.contract.functions.swapOffers(offer_id).call()
        seller = details[0]

        if seller == ADDRESS_ZERO:
            raise ValueError(f'Offer does not exist: {offer_id}')

        return {
            'seller': details[0],
            'oToken': details[1],
            'biddingToken': details[3],
            'minPrice': details[2],
            'minBidSize': details[4],
            'totalSize': details[5],
            'availableSize': details[6]
        }

    def validate_bid(self, bid: SignedBid) -> str:
        """
        Method to validate bid

        Args:
            bid (dict): Bid dictionary containing swapId, nonce, signerWallet,
              sellAmount, buyAmount, referrer, v, r, and s

        Raises:
            TypeError: Bid argument is not an instance of SignedBid

        Returns:
            response (dict): Dictionary containing number of errors (errors)
              and the corresponding error messages (messages)
        """
        if not isinstance(bid, SignedBid):
            raise TypeError("Invalid signed bid")

        bid.signerWallet = get_address(bid.signerWallet)
        bid.referrer = get_address(bid.referrer)

        response = self.contract.functions.check(asdict(bid)).call()

        errors = response[0]
        if errors == 0:
            return {"errors": 0}
        else:
            return {
                "errors": errors,
                "messages": [
                    Web3.toText(msg).replace("\x00", "")
                    for msg in response[1][:errors]
                ],
            }

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

        offer.oToken = get_address(offer.oToken)
        offer.biddingToken = get_address(offer.biddingToken)

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
            return self.contract.events.NewOffer() \
                .processReceipt(tx_receipt)[0]["args"]["swapId"]

        
