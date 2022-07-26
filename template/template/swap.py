""" Module to call Swap contract """
from sdk_commons.config import OfferDetails
from template.definitions import ContractConfig, Offer, SignedBid
from template.wallet import Wallet


class SwapContract:
    """
    Object to create connection to the Swap contract

    Args:
        config (ContractConfig): Configuration to setup the Contract
    """

    def __init__(self, config: ContractConfig):
        ...

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

        # if not valid offer:
        #     raise ValueError(f'Offer does not exist: {offer_id}')

        return {
            'seller': "...",
            'oToken': "...",
            'biddingToken': "...",
            'minPrice': "...",
            'minBidSize': "...",
            'totalSize': "...",
            'availableSize': "...",
        }

    def validate_bid(self, bid: SignedBid) -> str:
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

        ...
        return 'error'

    def create_offer(self, offer: Offer, wallet: Wallet) -> str:
        """
        Method to create offer

        Args:
            offer (dict): Offer dictionary containing necessary
                          parameters to create a new offer
            wallet (Wallet): Wallet class instance

        Raises:
            TypeError: Offer argument is an Offer class instance
            ExecError: Transaction reverted

        Returns:
            offerId (int): OfferId of the created order
        """
        if not isinstance(offer, Offer):
            raise TypeError("Invalid offer")

        return "offer"
