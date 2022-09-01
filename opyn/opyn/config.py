from typing import Any

from opyn.definitions import BidData, ContractConfig, Domain, MessageToSign, Offer
from opyn.otoken import oTokenContract
from opyn.settlement import SettlementContract
from opyn.wallet import Wallet
from sdk_commons.chains import Chains
from sdk_commons.config import BidValidation, OfferDetails, OfferTokenDetails, SDKConfig
from sdk_commons.helpers import get_evm_signature_components


class AuthorizationPages:
    mainnet = "https://notdefined.yet/auctions/"
    testnet = "https://notdefined.yet/auctions/"


class OpynSDKConfig(SDKConfig):

    authorization_pages = AuthorizationPages
    supported_chains = [
        Chains.ETHEREUM,
        Chains.ROPSTEN,
    ]

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

        swap_contract = SettlementContract(config)

        new_offer = Offer(
            offerToken=oToken,
            bidToken=bidding_token,
            minBidSize=min_bid_size,
            minPrice=min_price,
            totalSize=offer_amount,
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
        swap_contract = SettlementContract(swap_config)
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

        domain = Domain(
            name="OPYN BRIDGE",
            version="1",
            chainId=chain_id,
            verifyingContract=contract_address,
        )

        # TODO: use the provided nonce instead of retrieve on-chain?
        rpc_uri = "not-currently-provided"
        settlement_config = ContractConfig(contract_address, rpc_uri, Chains(chain_id))
        settlement_contract = SettlementContract(settlement_config)
        maker_nonce = settlement_contract.nonce(public_key)

        payload = MessageToSign(
            offerId=1,
            # This field is missing
            bidId=0,
            signerAddress=public_key,
            bidderAddress=public_key,
            bidToken="...",
            offerToken="...",
            bidAmount=buy_amount,
            sellAmount=sell_amount,
            nonce=maker_nonce,
        )

        wallet = Wallet(public_key=public_key, private_key=private_key)
        signed_bid = wallet.sign_bid_data(domain, payload)

        return signed_bid.r[2:] + signed_bid.s[2:] + hex(signed_bid.v)[2:]

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
        swap_contract = SettlementContract(config)

        # Expected to fail: BidData currently has a different signature
        signed_bid = BidData(
            offerId=swap_id,
            # This field is missing
            bidId=0,
            # nonce=nonce,
            signerAddress=signer_wallet,
            # These three fields are missing
            bidderAddress="...",
            bidToken="...",
            offerToken="...",
            bidAmount=buy_amount,
            sellAmount=sell_amount,
            # referrer=referrer,
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
