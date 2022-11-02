import json
from decimal import Decimal
from typing import Any

import web3

from sdk_commons.chains import Chains
from sdk_commons.config import BidValidation, OfferDetails, OfferTokenDetails, SDKConfig
from template.definitions import Bid
from template.wallet import Wallet


class AuthorizationPages:
    mainnet = "https://thetanuts.finance/paradigm/mm-approval"
    polygon = "https://thetanuts.finance/paradigm/mm-matic-approval"


class TemplateSDKConfig(SDKConfig):

    authorization_pages = AuthorizationPages
    supported_chains = [Chains.MAINNET, Chains.MATIC]

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
        return int(oToken[2:], 16)

    def get_otoken_details(
        self,
        *,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        **kwargs: Any,
    ) -> OfferTokenDetails:
        """Return details about the offer token"""

        w3 = web3.Web3(web3.HTTPProvider(rpc_uri))
        bridgeContract = w3.eth.contract(
            w3.toChecksumAddress(contract_address),
            abi=json.load(open("abis/ParadigmBridge.json", "r")),
        )

        aucDetails = bridgeContract.functions.getAuctionDetails(contract_address).call()

        return {
            "collateralAsset": aucDetails[0],
            "underlyingAsset": aucDetails[1],
            "strikeAsset": aucDetails[2],
            "strikePrice": Decimal(aucDetails[3]) / Decimal("1000000"),
            "expiryTimestamp": aucDetails[4],
            "isPut": aucDetails[5],
        }

    def get_offer_details(
        self,
        *,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        offer_id: int,
        **kwargs: Any,
    ) -> OfferDetails:
        """Return details for a given offer"""

        w3 = web3.Web3(web3.HTTPProvider(rpc_uri))
        bridgeContract = w3.eth.contract(
            w3.toChecksumAddress(contract_address),
            abi=json.load(open("abis/ParadigmBridge.json", "r")),
        )
        vault_address = "0x%040x" % offer_id

        try:
            aucDetails = bridgeContract.functions.getAuctionDetails(contract_address).call()
        except Exception:
            raise ValueError("The argument is not a valid offer")

        return {
            'seller': vault_address,
            'oToken': vault_address,
            'biddingToken': aucDetails[0],
            'minPrice': Decimal(0.0),
            'minBidSize': Decimal(aucDetails[5]) / Decimal("1000000"),
            'totalSize': Decimal(aucDetails[5]) / Decimal("1000000"),
            'availableSize': Decimal(aucDetails[5]) / Decimal("1000000"),
        }

    def sign_bid(
        self,
        *,
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
        **kwargs: Any,
    ) -> str:
        """Sign a bid and return the signature"""

        payload = Bid(
            swapId=swap_id,  # Vault address casted as integer
            nonce=nonce,  # expiryTimestamp
            signerWallet=signer_wallet,
            sellAmount=sell_amount,
            buyAmount=buy_amount,  # Only entire vault allowed, no partials
            referrer=referrer,
        )
        wallet = Wallet(public_key=public_key, private_key=private_key)
        signature = wallet.sign_bid(payload)

        return signature

    def validate_bid(
        self,
        *,
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
        **kwargs: Any,
    ) -> BidValidation:
        """Validate the signing bid"""

        w3 = web3.Web3(web3.HTTPProvider(rpc_uri))
        bridgeContract = w3.eth.contract(
            w3.toChecksumAddress(contract_address),
            abi=json.load(open("abis/ParadigmBridge.json", "r")),
        )

        isValid = bridgeContract.functions.validateSignature(
            hex(swap_id), nonce, sell_amount, signer_wallet, signature
        ).call()

        return {'errors': not isValid}

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

        w3 = web3.Web3(web3.HTTPProvider(rpc_uri))
        assert w3.eth.chainId == chain_id
        bidding_token = w3.eth.contract(
            w3.toChecksumAddress(token_address),
            abi=json.load(open("abis/ERC20.json", "r")),
        )

        allowance = bidding_token.functions.allowance(self.public_key, contract_address).call() / (
            10 ** bidding_token.functions.decimals().call()
        )

        return allowance > 1e30
