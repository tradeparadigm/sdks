from enum import Enum

from asgiref.sync import async_to_sync
from solana.publickey import PublicKey
from spl.token.instructions import get_associated_token_address

from friktion.friktion_anchor.accounts.swap_order import SwapOrder
from friktion.offer import Offer
from friktion.swap import Network, SwapContract
from sdk_commons.config import SDKConfig


class AuthorizationPages:
    # TODO: add when we get the UI for both
    mainnet = "https://notdefined.yet/auctions/"
    testnet = "https://notdefined.yet/auctions/"


# TODO: remove me
class Chains(Enum):
    SOLANA_DEV = 777777
    SOLANA_MAIN = 888888


class FriktionSDKConfig(SDKConfig):

    authorization_pages = AuthorizationPages
    # TODO: replace with:
    # supported_chains = [Chains.SOLANA_DEV]
    venue_chains = Chains

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
        **kwargs,
    ) -> str:
        """Create an offer"""

        swap_order = SwapOrder(...)
        Offer.from_swap_order(swap_order=swap_order, address=PublicKey(public_key))
        ...

    def get_otoken_details(
        self,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        offer_id: int,
        seller: str,
        **kwargs,
    ) -> dict:
        """Return details about the offer token"""

        network = self.CHAIN_NETWORK_MAP[chain_id]
        swap_contract = SwapContract(network)
        details = async_to_sync(swap_contract.get_offered_token_details)(
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
        **kwargs,
    ) -> dict:
        """Return details for a given offer"""

        network = self.CHAIN_NETWORK_MAP[chain_id]
        swap_contract = SwapContract(network)

        details: Offer = async_to_sync(swap_contract.get_offer_details)(
            PublicKey(seller), offer_id
        )
        return {
            'seller': str(details.seller),
            'bidding_token': str(details.biddingToken),
            'min_price': details.minPrice,
            'min_bid_size': details.minBidSize,
            'total_size': details.offerAmount,
            'offered_token': str(details.oToken),
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
        v: int,
        r: str,
        s: str,
        **kwargs,
    ) -> str:
        """Validate the signing bid"""

        return None

    def verify_allowance(
        self,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        public_key: str,
        token_address: str,
        **kwargs,
    ) -> bool:
        """
        Verify if the contract is allowed to access
        the given token on the wallet
        """

        network = self.CHAIN_NETWORK_MAP[chain_id]
        swap_contract = SwapContract(network)

        token_account = get_associated_token_address(
            PublicKey(public_key), PublicKey(token_address)
        )

        return swap_contract.verify_allowance(PublicKey(token_address), token_account)
