from opyn.definitions import BidData, ContractConfig, Offer
from opyn.otoken import oTokenContract
from opyn.settlement import SettlementContract
from opyn.wallet import Wallet
from sdk_commons.chains import Chains
from sdk_commons.config import SDKConfig


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
        **kwargs,
    ) -> str:
        """Create an offer"""

        wallet = Wallet(public_key=public_key, private_key=private_key)

        config = ContractConfig(address=contract_address, chain_id=chain_id, rpc_uri=rpc_uri)
        swap_contract = SettlementContract(config)

        new_offer = Offer(
            oToken=oToken,
            biddingToken=bidding_token,
            minBidSize=min_bid_size,
            minPrice=min_price,
            offerAmount=offer_amount,
        )
        return swap_contract.create_offer(new_offer, wallet)

    def get_otoken_details(
        self, contract_address: str, chain_id: int, rpc_uri: str, **kwargs
    ) -> dict:
        """Return details about the offer token"""
        config = ContractConfig(address=contract_address, chain_id=chain_id, rpc_uri=rpc_uri)
        otoken_contract = oTokenContract(config)
        return otoken_contract.get_otoken_details()

    def get_offer_details(
        self, contract_address: str, chain_id: int, rpc_uri: str, offer_id: int, **kwargs
    ) -> dict:
        """Return details for a given offer"""
        swap_config = ContractConfig(address=contract_address, chain_id=chain_id, rpc_uri=rpc_uri)
        swap_contract = SettlementContract(swap_config)
        return swap_contract.get_offer_details(offer_id)

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

        config = ContractConfig(address=contract_address, chain_id=chain_id, rpc_uri=rpc_uri)
        swap_contract = SettlementContract(config)

        # Expected to fail: BidData currently has a different signature
        signed_bid = BidData(
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
        **kwargs,
    ) -> bool:
        """
        Verify if the contract is allowed to access
        the given token on the wallet
        """

        config = ContractConfig(address=contract_address, chain_id=chain_id, rpc_uri=rpc_uri)
        wallet = Wallet(public_key=public_key)
        return wallet.verify_allowance(config, token_address=token_address)
