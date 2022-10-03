from typing import Any

from sdk_commons.chains import Chains
from sdk_commons.config import BidValidation, OfferDetails, OfferTokenDetails, SDKConfig
from sdk_commons.helpers import get_evm_signature_components
from template.definitions import Bid, ContractConfig, Offer, SignedBid
from template.otoken import oTokenContract
from template.swap import SwapContract
from template.wallet import Wallet

import web3, json

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

        return int( oToken[2:], 16 )

    """ ## Sample transaction sending

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
        
        w3 = web3.Web3(web3.HTTPProvider(rpc_uri));
        swap_contract = w3.eth.contract(w3.toChecksumAddress(contract_address), abi=json.load( open("abis/ParadigmBridge.json","r") ) ;

        tx = swap_contract.functions.createOffer( oToken )
        tx = tx.buildTransaction('nonce': w3.eth.getTransactionCount(public_key)})
        signed = w3.eth.account.sign_transaction(tx, PRVKEY)
        tx = w3_infura.eth.sendRawTransaction(signed.rawTransaction)
    ""


    def get_otoken_details(
        self,
        *,
        contract_address: str,
        chain_id: int,
        rpc_uri: str,
        **kwargs: Any,
    ) -> OfferTokenDetails:
        """Return details about the offer token"""

        config = ContractConfig(
            address=contract_address, chain_id=Chains(chain_id), rpc_uri=rpc_uri
        )

        w3 = web3.Web3(web3.HTTPProvider(rpc_uri));
        bridgeContract = w3.eth.contract(w3.toChecksumAddress(contract_address), abi=json.load( open("abis/ParadigmBridge.json","r") ) ;    
        
        aucDetails = bridgeContract.functions.getAuctionDetails( contract_address ).call()
        
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

        swap_config = ContractConfig(
            address=contract_address, chain_id=Chains(chain_id), rpc_uri=rpc_uri
        )

        swap_contract = SwapContract(swap_config)
        
        w3 = web3.Web3(web3.HTTPProvider(rpc_uri));
        bridgeContract = w3.eth.contract(w3.toChecksumAddress(contract_address), abi=json.load( open("abis/ParadigmBridge.json","r") ) ;
        vault_address = "0x%040"%offer_id
         
        try:
            bridgeContract.
            aucDetails = bridgeContract.functions.getAuctionDetails( contract_address ).call()
        except:
            raise ValueError("The argument is not a valid offer")
                    
        return {
            'seller': vault_address,
            'oToken': vault_address,
            'biddingToken': aucDetails[0],
            'minPrice': Decimal(0.0),
            'minBidSize': Decimal(0.0),
            'totalSize': Decimal(0.0),
            'availableSize': Decimal(0.0),
        }
        

    """
    from eth_abi.packed import encode_abi_packed
    from eth_account.messages import encode_defunct
    def quote(strikeX1e6, premium, collatAmt, targetExpiry, vault, designatedMaker):
        toSign = encode_abi_packed( ['uint[]', 'uint', 'uint', "uint", "address", "address"], [strikeX1e6, int(premium), int(collatAmt), int(targetExpiry), vault, designatedMaker.address] )
        signed = web3.eth.account.sign_message(encode_defunct(web3.keccak(toSign)), private_key=designatedMaker.private_key)
        sigHex = signed.signature.hex()
        return sigHex
    """
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

        config = ContractConfig(
            address=contract_address, chain_id=Chains(chain_id), rpc_uri=rpc_uri
        )

        wallet = Wallet(public_key=public_key)
        return wallet.verify_allowance(config, token_address=token_address)
