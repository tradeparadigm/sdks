from decimal import Decimal
from typing import Any

from asgiref.sync import async_to_sync
from solana.publickey import PublicKey
from spl.token.instructions import get_associated_token_address

# from friktion.friktion_anchor.accounts.swap_order import SwapOrder
from friktion.offer import Offer
from friktion.swap import Network, SwapContract
from sdk_commons.chains import Chains
from sdk_commons.config import BidValidation, OfferDetails, OfferTokenDetails, SDKConfig


class AuthorizationPages:
    mainnet = "https://app.friktion.fi/approve"
    testnet = "https://devnet.friktion.fi/approve"


class FriktionSDKConfig(SDKConfig):

    authorization_pages = AuthorizationPages
    supported_chains = [Chains.SOLANA_DEV]

    CHAIN_NETWORK_MAP = {
        Chains.SOLANA_DEV: Network.DEVNET,
        Chains.SOLANA_MAIN: Network.MAINNET,
    }

    def create_offer(
        self,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        oToken: str,
        bidding_token: str,
        min_price: int,
        min_bid_size: int,
        offer_amount: int,
        public_key: str,
        private_key: str,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        """Create an offer"""

        # swap_order = SwapOrder(...)
        # Offer.from_swap_order(
        #     swap_order=swap_order,
        #     address=PublicKey(public_key)
        # )

        return "not-implemented-yet"

    def get_otoken_details(
        self,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        offer_id: int,
        seller: str,
        *args: Any,
        **kwargs: Any,
    ) -> OfferTokenDetails:
        """Return details about the offer token"""

        network = self.CHAIN_NETWORK_MAP[Chains(chain_id)]
        swap_contract = SwapContract(network)
        details: OfferTokenDetails = async_to_sync(swap_contract.get_offered_token_details)(
            PublicKey(seller), offer_id
        )

        return details

    def get_offer_details(
        self,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        offer_id: int,
        seller: str,
        *args: Any,
        **kwargs: Any,
    ) -> OfferDetails:
        """Return details for a given offer"""

        network = self.CHAIN_NETWORK_MAP[Chains(chain_id)]
        swap_contract = SwapContract(network)

        details: Offer = async_to_sync(swap_contract.get_offer_details)(
            PublicKey(seller), offer_id
        )
        # TODO: enforce specific types on OfferDetails
        return {
            'seller': str(details.seller),
            'biddingToken': str(details.biddingToken),
            'minPrice': str(details.minPrice),
            'minBidSize': Decimal(details.minBidSize),
            'totalSize': Decimal(details.offerAmount),
            'oToken': str(details.oToken),
            'availableSize': "???",
        }

    def validate_bid(
        self,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        swap_id: int,
        nonce: int,
        signer_wallet: str,
        sell_amount: int,
        buy_amount: int,
        referrer: str,
        signature: str,
        *args: Any,
        **kwargs: Any,
    ) -> BidValidation:
        """Validate the signing bid"""

        return {'errors': 0}

    def verify_allowance(
        self,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        public_key: str,
        token_address: str,
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        """
        Verify if the contract is allowed to access
        the given token on the wallet
        """

        network = self.CHAIN_NETWORK_MAP[Chains(chain_id)]
        swap_contract = SwapContract(network)

        token_account = get_associated_token_address(
            PublicKey(public_key), PublicKey(token_address)
        )

        return swap_contract.verify_allowance(PublicKey(token_address), token_account)
