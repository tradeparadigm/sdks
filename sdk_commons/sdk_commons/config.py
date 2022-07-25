import abc


class SDKConfig(abc.ABC):
    """
    This is the abstract common interface that every venues
    are expended to implement. Each method will be invoked by
    API providing all listed parameters but each venue is free
    to only include needed parameters in their own concrete
    implementation. All additional parameters will be consumed by
    **kwargs that is always expected to be included.
    A template venue is also provided as example for a concrete
    implementation.
    """

    def __init__(self, contract_address: str, chain_id: int, rpc_uri: str, **kwargs):
        self.contract_address = contract_address
        self.chain_id = chain_id
        self.rpc_uri = rpc_uri

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
    def venue_chains(self):
        """
        Set this property with an Enum
        listing all supported chains
        """
        pass

    @abc.abstractmethod
    def create_offer(
        self,
        # TODO: rename into offer_token
        oToken: str,
        bidding_token: str,
        min_price: int,
        min_bid_size: int,
        offer_amount: int,
        public_key: str,
        private_key: str,
        **kwargs,
    ) -> str:
        """
        Create an offer
        """

    # TODO: rename into get_offered_token_details
    @abc.abstractmethod
    def get_otoken_details(self, **kwargs) -> dict:
        """
        Return details about the offer token
        """

    @abc.abstractmethod
    def get_offer_details(self, offer_id: int, **kwargs) -> dict:
        """Return details for a given offer"""

    @abc.abstractmethod
    def validate_bid(
        self,
        swap_id: int,
        nonce: int,
        signer_wallet: str,
        sell_amount: int,
        buy_amount: int,
        referrer: str,
        v: int,
        r: str,
        s: str,
        **kwargs,
    ) -> str:
        """Validate the signing bid"""

    @abc.abstractmethod
    def verify_allowance(
        self,
        public_key: str,
        token_address: str,
        **kwargs,
    ) -> bool:
        """
        Verify if the contract is allowed to access
        the given token on the wallet
        """
