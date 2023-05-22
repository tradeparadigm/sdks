#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# Created By: Steven@Ribbon, Paolo@Paradigm
# Created Date: 04/04/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module to call Swap contract """
# ---------------------------------------------------------------------------

from dataclasses import asdict
from shutil import ExecError
from typing import cast

from web3 import Web3
from web3.types import TxParams

from ribbon.contract import ContractConnection
from ribbon.definitions import Offer, SignedBid
from ribbon.encode import ADDRESS_ZERO
from ribbon.utils import get_address
from ribbon.wallet import Wallet
from sdk_commons.chains import Chains
from sdk_commons.config import BidValidation, OfferDetails

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DETAILED_ERROR_MESSAGES = {
    "SIGNATURE_INVALID": "Signature invalid.",
    "UNAUTHORIZED": (
        "Signer address in bid differs from signatory. "
        "Either ensure the signer wallet has authorized signatory if using a delegate, "
        "or ensure the signed message details are accurate."
    ),
    "NONCE_ALREADY_USED": "This nonce has been previously used.",
    "BID_TOO_SMALL": "Bid size has to be larger than minimum bid.",
    "BID_EXCEED_AVAILABLE_SIZE": "Bid size has to be smaller than available size.",
    "PRICE_TOO_LOW": "Price per oToken has to be larger than minimum price.",
    "SIGNER_ALLOWANCE_LOW": (
        "Insufficient bidding token allowance. "
        "Ensure you have approved sufficient amount of bidding token."
    ),
    "SIGNER_BALANCE_LOW": (
        "Insufficient bidding token balance. "
        "Ensure you have sufficient balance of bidding token in your wallet."
    ),
}

GAS_LIMIT = 200000


# ---------------------------------------------------------------------------
# Swap Contract
# ---------------------------------------------------------------------------
class SwapContract(ContractConnection):
    """
    Object to create connection to the Swap contract

    Args:
        config (ContractConfig): Configuration to setup the Contract
    """

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
            'availableSize': details[6],
        }

    def validate_bid(self, bid: SignedBid) -> BidValidation:
        """
        Method to validate bid

        Args:
            bid (dict): Bid dictionary containing swapId, nonce,
                        signerWallet, sellAmount, buyAmount,
                        referrer, v, r, and s

        Raises:
            TypeError: Bid argument is not an instance of SignedBid

        Returns:
            response (dict): Dictionary containing number of errors
              and the corresponding error messages
        """
        if not isinstance(bid, SignedBid):
            raise TypeError("Invalid signed bid")

        if bid.v is None:
            raise TypeError("Invalid signed bid, missing v")

        bid.signerWallet = get_address(bid.signerWallet)
        bid.referrer = get_address(bid.referrer)
        bid.v = bid.v + (bid.v < 27) * 27

        response = self.contract.functions.check(asdict(bid)).call()

        errors = response[0]
        if errors == 0:
            return {"errors": 0}
        else:
            return {
                "errors": errors,
                "messages": [
                    DETAILED_ERROR_MESSAGES[Web3.to_text(msg).replace("\x00", "")]
                    for msg in response[1][:errors]
                ],
            }

    def validate_authority(self, wallet: Wallet, authority_address: str) -> bool:
        """
        Method to verify authority

        Args:
            wallet_address (str): Address of the wallet
            authority_address (str): Address of the authority

        Returns:
            verified (bool): True if the authority is set for the wallet
        """
        authorized = cast(str, self.contract.functions.authorized(wallet.public_key).call())
        return authorized == authority_address

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

        offer.oToken = get_address(offer.oToken)
        offer.biddingToken = get_address(offer.biddingToken)

        nonce = self.w3.eth.get_transaction_count(Web3.to_checksum_address(wallet.public_key))
        tx_params: TxParams = {}
        if self.config.chain_id in [Chains.BSC, Chains.BSC_TESTNET]:
            # BSC transactions require the gasPrice parameter
            tx_params = {
                "nonce": nonce,
                "gas": GAS_LIMIT,
                'gasPrice': self.w3.eth.gas_price,
            }
        else:
            tx_params = {"nonce": nonce, "gas": GAS_LIMIT}
        tx = self.contract.functions.createOffer(*list(asdict(offer).values())).build_transaction(
            tx_params
        )

        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=wallet.private_key)

        self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        tx_receipt = self.w3.eth.wait_for_transaction_receipt(signed_tx.hash, timeout=600)

        if tx_receipt["status"] == 0:
            raise ExecError(f'Transaction reverted: {signed_tx.hash.hex()}')

        return cast(
            str, self.contract.events.NewOffer().process_receipt(tx_receipt)[0]["args"]["swapId"]
        )
