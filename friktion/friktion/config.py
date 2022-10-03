import logging
from decimal import Decimal
from typing import Any

from anchorpy import Wallet
from asgiref.sync import async_to_sync
from solana.keypair import Keypair
from solana.publickey import PublicKey

from friktion.bid_details import BidDetails
from friktion.offer import Offer
from friktion.swap import Network, SwapContract
from sdk_commons.chains import Chains
from sdk_commons.config import BidValidation, OfferDetails, OfferTokenDetails, SDKConfig

# from friktion.friktion_anchor.accounts.swap_order import SwapOrder

logger = logging.getLogger(__name__)


class AuthorizationPages:
    mainnet = "https://app.friktion.fi/approve"
    testnet = "https://devnet.friktion.fi/approve"


# TODO: remove unused parameters (for example rpc_uri and nonce)


class FriktionSDKConfig(SDKConfig):

    authorization_pages = AuthorizationPages
    supported_chains = [Chains.SOLANA_DEV, Chains.SOLANA_MAIN]

    CHAIN_NETWORK_MAP = {
        Chains.SOLANA_DEV: Network.DEVNET,
        Chains.SOLANA_MAIN: Network.MAINNET,
    }

    def create_offer(
        self,
        *,
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
        *,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        offer_id: int,
        seller: str,
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
        *,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        offer_id: int,
        seller: str,
        **kwargs: Any,
    ) -> OfferDetails:
        """Return details for a given offer"""

        network = self.CHAIN_NETWORK_MAP[Chains(chain_id)]
        swap_contract = SwapContract(network)

        details: Offer = async_to_sync(swap_contract.get_offer_details)(
            PublicKey(seller), offer_id
        )
        return {
            'seller': str(details.seller),
            'biddingToken': str(details.biddingToken),
            # NOTE: it is not a Decimal at this point
            # as we still have to apply the resolution.
            'minPrice': str(details.minPrice),
            'minBidSize': Decimal(details.minBidSize),
            'totalSize': Decimal(details.offerAmount),
            'oToken': str(details.oToken),
            'availableSize': "???",
        }

    def sign_bid(
        self,
        *,
        private_key: str,
        swap_id: int,
        signer_wallet: str,
        sell_amount: int,
        buy_amount: int,
        referrer: str,
        **kwargs: Any,
    ) -> str:
        """Sign a bid and return the signature"""

        if 'creator' not in kwargs:
            raise Exception("Creator is required")

        bid = BidDetails(
            bid_size=buy_amount,
            referrer=PublicKey(referrer),
            # TODO: replace this if necessary
            creator=kwargs['creator'],
            bid_price=sell_amount // buy_amount,
            signer_wallet=PublicKey(signer_wallet),
            order_id=swap_id,
        )

        wallet = Wallet(Keypair(solders.keypair.Keypair.from_base58_string(private_key)))
        _, signature = bid.as_signed_msg(wallet)

        return str(signature)

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


        if 'creator' not in kwargs:
            raise Exception("Creator is required")

        # TODO: consider changing sdk BidDetails to receive sell amount
        # instead of bid_price to avoid the reverse computation
        bid_price = int(sell_amount / buy_amount)
        bid_details = BidDetails(
            bid_price=bid_price,
            bid_size=buy_amount,
            order_id=swap_id,
            # TODO: replace this if necessary
            creator=kwargs['creator'],
            referrer=PublicKey(referrer),
            signer_wallet=PublicKey(signer_wallet),
        )

        network = self.CHAIN_NETWORK_MAP[Chains(chain_id)]
        swap_contract = SwapContract(network)
        error: str = async_to_sync(swap_contract.validate_bid)(
            PublicKey(seller), bid_details, signature
        )

        if error:
            return {'errors': 1, 'messages': [error]}

        return {'errors': 0}

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
        network = self.CHAIN_NETWORK_MAP[Chains(chain_id)]
        swap_contract = SwapContract(network)

        try:
            return swap_contract.verify_allowance(PublicKey(token_address), PublicKey(public_key))
        except BaseException:
            logger.exception(
                f"Failed to verify wallet allowance: token={token_address} wallet={public_key}"
            )
            return False
