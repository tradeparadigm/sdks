from sdk_commons.config import SDKConfig
from template.chains import Chains
from template.definitions import ContractConfig, Offer, SignedBid
from template.otoken import oTokenContract
from template.swap import SwapContract
from template.wallet import Wallet


class AuthorizationPages:
    mainnet = "https://..."
    testnet = "https://..."


class TemplateSDKConfig(SDKConfig):

    authorization_pages = AuthorizationPages
    venue_chains = Chains

    def create_offer(
        self,
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

        wallet = Wallet(public_key=public_key, private_key=private_key)

        config = ContractConfig(
            address=self.contract_address, chain_id=self.chain_id, rpc_uri=self.rpc_uri
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

    def get_otoken_details(self, **kwargs) -> dict:
        """Return details about the offer token"""
        config = ContractConfig(
            address=self.contract_address, chain_id=self.chain_id, rpc_uri=self.rpc_uri
        )
        otoken_contract = oTokenContract(config)
        return otoken_contract.get_otoken_details()

    def get_offer_details(self, offer_id: int, **kwargs) -> dict:
        """Return details for a given offer"""
        swap_config = ContractConfig(
            address=self.contract_address, chain_id=self.chain_id, rpc_uri=self.rpc_uri
        )
        swap_contract = SwapContract(swap_config)
        return swap_contract.get_offer_details(offer_id)

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

        config = ContractConfig(
            address=self.contract_address, chain_id=self.chain_id, rpc_uri=self.rpc_uri
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
        public_key: str,
        token_address: str,
        **kwargs,
    ) -> bool:
        """
        Verify if the contract is allowed to access
        the given token on the wallet
        """

        config = ContractConfig(
            address=self.contract_address, chain_id=self.chain_id, rpc_uri=self.rpc_uri
        )
        wallet = Wallet(public_key=public_key)
        return wallet.verify_allowance(config, token_address=token_address)
