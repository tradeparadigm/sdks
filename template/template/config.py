from typing import Any

from sdk_commons.chains import Chains
from sdk_commons.config import BidValidation, OfferDetails, OfferTokenDetails, SDKConfig
from sdk_commons.helpers import get_evm_signature_components
from template.definitions import Bid, ContractConfig, Offer, SignedBid
from template.otoken import oTokenContract
from template.swap import SwapContract
from template.wallet import Wallet


class AuthorizationPages:
    mainnet = "https://..."
    testnet = "https://..."


class TemplateSDKConfig(SDKConfig):

    authorization_pages = AuthorizationPages
    supported_chains = [Chains.ROPSTEN, Chains.KOVAN]

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

        wallet = Wallet(public_key=public_key, private_key=private_key)

        config = ContractConfig(
            address=contract_address, chain_id=Chains(chain_id), rpc_uri=rpc_uri
        )

        swap_contract = SwapContract(config)

        new_offer = Offer(
            oToken=oToken,
            biddingToken=bidding_token,
            minBidSize=min_bid_size,
            minPrice=min_price,
            offerAmount=offer_amount,
        )
        return swap_contract.create_offer(new_offer, wallet)

    def get_otoken_details(
        self,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        *args: Any,
        **kwargs: Any,
    ) -> OfferTokenDetails:
        """Return details about the offer token"""

        config = ContractConfig(
            address=contract_address, chain_id=Chains(chain_id), rpc_uri=rpc_uri
        )

        otoken_contract = oTokenContract(config)
        return otoken_contract.get_otoken_details()

    def get_offer_details(
        self,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        offer_id: int,
        *args: Any,
        **kwargs: Any,
    ) -> OfferDetails:
        """Return details for a given offer"""

        swap_config = ContractConfig(
            address=contract_address, chain_id=Chains(chain_id), rpc_uri=rpc_uri
        )

        swap_contract = SwapContract(swap_config)
        return swap_contract.get_offer_details(offer_id)

    def sign_bid(
        self,
        contract_address: str,
        chain_id: int,
        public_key: str,
        private_key: str,
        swap_id: int,
        nonce: int,
        signer_wallet: str,
        sell_amount: int,
        buy_amount: int,
        referrer: str,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        """Sign a bid and return the signature"""

        payload = Bid(
            swapId=swap_id,
            nonce=nonce,
            signerWallet=signer_wallet,
            sellAmount=sell_amount,
            buyAmount=buy_amount,
            referrer=referrer,
        )
        wallet = Wallet(public_key=public_key, private_key=private_key)
        signature = wallet.sign_bid(payload)

        return signature

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
        r, s, v = get_evm_signature_components(signature)

        config = ContractConfig(
            address=contract_address,
            chain_id=Chains(chain_id),
            rpc_uri=rpc_uri,
        )

        swap_contract = SwapContract(config)

        signed_bid = SignedBid(
            swapId=swap_id,
            nonce=nonce,
            signerWallet=signer_wallet,
            sellAmount=sell_amount,
            buyAmount=buy_amount,
            referrer=referrer,
            r=r,
            s=s,
            v=v,
        )
        return swap_contract.validate_bid(signed_bid)

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

        config = ContractConfig(
            address=contract_address, chain_id=Chains(chain_id), rpc_uri=rpc_uri
        )

        wallet = Wallet(public_key=public_key)
        return wallet.verify_allowance(config, token_address=token_address)
