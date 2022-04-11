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

from contract import ContractConnection
from definitions import SignedBid
from utils import get_address
from encode import ADDRESS_ZERO


# ---------------------------------------------------------------------------
# Swap Contract
# ---------------------------------------------------------------------------
class SwapContract(ContractConnection):
    """
    Object to create connection to the Swap contract

    Args:
        config (ContractConfig): Configuration to setup the Contract
    """

    def get_offer_details(self, id: int) -> dict:
        """
        Method to get bid details

        Args:
            id (int): Offer ID

        Raises:
            TypeError: Bid argument is not an instance of SignedBid

        Returns:
            details (dict): Offer details
        """
        details = self.contract.functions.swapOffers(id).call()
        seller = details[0]
        
        if seller == ADDRESS_ZERO:
            raise ValueError(f'Offer does not exist: {id}')
        
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
