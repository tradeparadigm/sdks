import abc
from decimal import Decimal
from typing import Any, TypedDict

from sdk_commons.chains import Chains


class OfferDetails(TypedDict):
    # TODO: enforce specific types?
    seller: str
    oToken: str
    biddingToken: str
    minPrice: str
    minBidSize: Decimal
    totalSize: Decimal
    availableSize: str


class OfferTokenDetails(TypedDict):
    # TODO: enforce specific types?
    collateralAsset: str
    underlyingAsset: str
    strikeAsset: str
    # TODO: should be a Decimal?
    # strike_price in friktion.swap.get_offered_token_details
    # is computed as 333333333.3333333, if converted to decimal we get
    # 333333333.333333313465118408203125 that is unexpectedly long
    # Introduce a rounding?
    strikePrice: float
    # expiration in seconds since epoch
    expiryTimestamp: int
    isPut: bool


class BidValidation(TypedDict, total=False):
    errors: int
    messages: list[str]


class SDKConfig(abc.ABC):
    """
    This is the abstract common interface that every venues
    are expected to implement. Each method will be invoked by
    API providing all listed parameters but each venue is free
    to only include needed parameters in their own concrete
    implementation. All additional parameters will be consumed by
    **kwargs that is always expected to be included.

    A template venue is also provided as example for a concrete
    implementation.
    """

    # TODO: consider to replace this class with the properties
    # - mainnet_authorization_page
    # - testnet_authorization_page
    # To have easier safe types
    @property
    @abc.abstractmethod
    def authorization_pages(self):
        """
        Set this property with a class containing
        mainnet and testnet properties
        """
        pass

    @property
    @abc.abstractmethod
    def supported_chains(self) -> list[Chains]:
        """
        Set this property with a list
        of all supported chains
        """
        pass

    @abc.abstractmethod
    def create_offer(
        self,
        *,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        # TODO: rename into offer_token
        oToken: str,
        bidding_token: str,
        min_price: int,
        min_bid_size: int,
        offer_amount: int,
        public_key: str,
        private_key: str,
        **kwargs: Any,
    ) -> str:
        """
        Create an offer
        """

    # TODO: rename into get_offered_token_details
    @abc.abstractmethod
    def get_otoken_details(
        self,
        *,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        offer_id: int,
        seller: str,
        **kwargs: Any,
    ) -> OfferTokenDetails:
        """
        Return details about the offer token
        """

    @abc.abstractmethod
    def get_offer_details(
        self,
        *,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        offer_id: int,
        seller: str,
        **kwargs: Any,
    ) -> OfferDetails:
        """Return details for a given offer"""

    @abc.abstractmethod
    def validate_bid(
        self,
        *,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        seller: str,
        swap_id: int,
        nonce: int,
        signer_wallet: str,
        sell_amount: int,
        buy_amount: int,
        referrer: str,
        signature: str,
        **kwargs: Any,
    ) -> BidValidation:
        """Validate the signing bid"""

    @abc.abstractmethod
    def verify_allowance(
        self,
        *,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        public_key: str,
        token_address: str,
        **kwargs: Any,
    ) -> bool:
        """
        Verify if the contract is allowed to access
        the given token on the wallet
        """
