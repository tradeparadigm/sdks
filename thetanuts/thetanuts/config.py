import time
from typing import Any

import web3
from web3.middleware import geth_poa_middleware
from web3.types import Nonce

from sdk_commons.chains import Chains
from sdk_commons.config import BidValidation, OfferDetails, OfferTokenDetails, SDKConfig
from sdk_commons.helpers import get_abi
from thetanuts.definitions import Bid
from thetanuts.wallet import Wallet


class AuthorizationPages:
    mainnet = "https://thetanuts.finance/paradigm/mm-approval"
    polygon = "https://thetanuts.finance/paradigm/mm-matic-approval"
    testnet = "https://thetanuts.finance/paradigm/mm-matic-approval"


class Thetanuts(SDKConfig):
    authorization_pages = AuthorizationPages
    supported_chains = [Chains.ETHEREUM, Chains.MATIC]
    PARADIGM_OFFSET = 100  # Bridge returns 1e6, Paradigm expects 1e8
    PRIORITY_FEE = {Chains.ETHEREUM: hex(int(1e8)), Chains.MATIC: hex(int(30e9))}

    def create_offer(
        self,
        *,
        contract_address: str,
        chain_id: Chains,
        rpc_uri: str,
        oToken: str,
        bidding_token: str,
        public_key: str,
        private_key: str,
        **kwargs: Any,
    ) -> str:
        """
        Start new round by forcefully ending previous round
        Needs to be done by Vault Owner
        """

        w3 = web3.Web3(web3.HTTPProvider(rpc_uri))
        if chain_id == Chains.MATIC:
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        vaultContract = w3.eth.contract(
            w3.to_checksum_address(oToken),
            abi=get_abi("Thetanuts_Vault"),
        )

        nonce = w3.eth.get_transaction_count(w3.to_checksum_address(public_key))

        if vaultContract.functions.expiry().call() > 0:  # Round in progress, let's end it
            currentTime = int(time.time())
            tx = w3.eth.send_raw_transaction(
                w3.eth.account.sign_transaction(
                    vaultContract.functions.setExpiry(currentTime).build_transaction(
                        {
                            'nonce': Nonce(nonce),
                            'from': public_key,
                            'maxPriorityFeePerGas': self.PRIORITY_FEE[chain_id],
                            'maxFeePerGas': hex(w3.eth.gas_price * 2),
                        }
                    ),
                    private_key,
                ).rawTransaction
            )
            print("Sent OWNER transaction for setting expiry", tx.hex())
            w3.eth.wait_for_transaction_receipt(tx)
            time.sleep(5)
            tx = w3.eth.send_raw_transaction(
                w3.eth.account.sign_transaction(
                    vaultContract.functions.settleStrike_MM(int(1000e6)).build_transaction(
                        {
                            'nonce': Nonce(nonce + 1),
                            'from': public_key,
                            'maxPriorityFeePerGas': self.PRIORITY_FEE[chain_id],
                            'maxFeePerGas': hex(w3.eth.gas_price * 2),
                        }
                    ),
                    private_key,
                ).rawTransaction
            )
            print("Sent OWNER transaction for settling vault", tx.hex())
            w3.eth.wait_for_transaction_receipt(tx)
            time.sleep(5)
            nonce = Nonce(nonce + 2)

        # Configure ParadigmBridge
        bridgeContract = w3.eth.contract(
            w3.to_checksum_address(contract_address),
            abi=get_abi("Thetanuts_ParadigmBridge"),
        )

        # Do Once! Configure ParadigmBridge to accept this vault
        # w3.eth.send_raw_transaction(
        #  w3.eth.account.sign_transaction(
        #   bridgeContract.functions.addVault( oToken, bidding_token )
        #    .build_transaction(
        #     {
        #      'nonce': w3.eth.get_transaction_count(public_key),
        #      'from':public_key
        #     }
        #    ), private_key
        #  ).rawTransaction
        # )

        # Initiate new round details for ParadigmBridge
        if (
            bridgeContract.functions.vaultNextStrikeX1e6(oToken).call() == 0
        ):  # New round not configured yet
            try:  # Optimistically assume CALL vault
                price = 4000e6  # Strike Price to sell at (multiplied by 1e6)
                amtToSell = vaultContract.functions.initNewRound([int(price)], 0, 0).call(
                    {"from": vaultContract.functions.designatedMaker().call()}
                )  # Get active balance in vault - will fail if not ready
            except Exception:  # If failed, assume PUT vault
                price = 1000e6  # Strike Price to sell at (multiplied by 1e6)
                amtToSell = vaultContract.functions.initNewRound([int(price)], 0, 0).call(
                    {"from": vaultContract.functions.designatedMaker().call()}
                )  # Get active balance in vault - will fail if not ready
            tx = w3.eth.send_raw_transaction(
                w3.eth.account.sign_transaction(
                    bridgeContract.functions.setNextStrikeAndSize(
                        oToken, int(price), amtToSell
                    ).build_transaction(
                        {
                            'nonce': Nonce(nonce),
                            'from': public_key,
                            "gas": 200000,
                            "maxPriorityFeePerGas": self.PRIORITY_FEE[chain_id],
                            'maxFeePerGas': hex(w3.eth.gas_price * 2),
                        }
                    ),
                    private_key,
                ).rawTransaction
            )
            print("Sent OWNER transaction for setting new strike and size", tx.hex())
            w3.eth.wait_for_transaction_receipt(tx)
            time.sleep(5)
        return str(
            (bridgeContract.functions.vaultIndexToAddress(contract_address).call() << 16)
            + vaultContract.functions.epoch().call()
            + 1
        )

    def get_otoken_details(
        self,
        *,
        # TODO: to be renamed into token_address
        contract_address: str,
        # TODO: to be normalized with the other methods
        swap_contract_address: str,
        chain_id: Chains,
        rpc_uri: str,
        **kwargs: Any,
    ) -> OfferTokenDetails:
        """Return details about the offer token"""

        w3 = web3.Web3(web3.HTTPProvider(rpc_uri))
        bridgeContract = w3.eth.contract(
            w3.to_checksum_address(swap_contract_address),
            abi=get_abi("Thetanuts_ParadigmBridge"),
        )

        aucDetails = bridgeContract.functions.getAuctionDetails(contract_address).call()

        return {
            "collateralAsset": aucDetails[0],
            "underlyingAsset": aucDetails[1],
            "strikeAsset": aucDetails[2],
            "strikePrice": aucDetails[3] * self.PARADIGM_OFFSET,
            "expiryTimestamp": aucDetails[4],
            "isPut": aucDetails[5],
        }

    def get_offer_details(
        self,
        *,
        contract_address: str,
        chain_id: Chains,
        rpc_uri: str,
        offer_id: int,
        **kwargs: Any,
    ) -> OfferDetails:
        """Return details for a given offer"""

        w3 = web3.Web3(web3.HTTPProvider(rpc_uri))
        bridgeContract = w3.eth.contract(
            w3.to_checksum_address(contract_address),
            abi=get_abi("Thetanuts_ParadigmBridge"),
        )

        vault_address = w3.to_checksum_address(
            bridgeContract.functions.vaultIndex(int(offer_id >> 16)).call()
        )

        try:
            aucDetails = bridgeContract.functions.getAuctionDetails(vault_address).call()
        except Exception:
            raise ValueError("The argument is not a valid offer")

        return {
            'seller': vault_address,
            'oToken': vault_address,
            'biddingToken': aucDetails[0],
            'minPrice': "0.0",
            'minBidSize': aucDetails[6] * self.PARADIGM_OFFSET,
            'totalSize': aucDetails[6] * self.PARADIGM_OFFSET,
            'availableSize': aucDetails[6] * self.PARADIGM_OFFSET,
        }

    def sign_bid(
        self,
        *,
        contract_address: str,
        chain_id: Chains,
        rpc_uri: str,
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
            vaultAddress=contract_address,  # Vault address casted as integer
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
        chain_id: Chains,
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
            w3.to_checksum_address(contract_address),
            abi=get_abi("Thetanuts_ParadigmBridge"),
        )
        vault_address = w3.to_checksum_address(
            bridgeContract.functions.vaultIndex(int(swap_id >> 16)).call()
        )

        vault = w3.eth.contract(vault_address, abi=get_abi("Thetanuts_Vault"))

        bidding_token = w3.eth.contract(
            w3.to_checksum_address(vault.functions.COLLAT().call()),
            abi=get_abi("ERC20"),
        )

        # Check for sufficient assets in wallet
        assetBalance = bidding_token.functions.balanceOf(signer_wallet).call()
        if assetBalance < sell_amount:
            return {'errors': 1, "messages": ["insufficient bidding token in wallet"]}

        # Metamask returns a signature string without '0x' prepend
        if signature[0:2].lower() != "0x":
            signature = "0x" + signature

        # Check for valid signature
        try:
            isValid = bridgeContract.functions.validateSignature(
                vault_address,
                nonce,
                sell_amount,
                w3.to_checksum_address(signer_wallet),
                signature,
            ).call()
        except Exception:  # Catches revert when signature invalid
            return {'errors': 1, "messages": ["signature invalid"]}

        if isValid:
            return {'errors': 0}
        else:
            return {'errors': 1, "messages": ["signature valid, bid parameters invalid"]}

    def verify_allowance(
        self,
        *,
        contract_address: str,
        chain_id: Chains,
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
        if not w3.eth.chain_id == chain_id.value:
            return False

        bidding_token = w3.eth.contract(
            w3.to_checksum_address(token_address),
            abi=get_abi("ERC20"),
        )

        allowance = bidding_token.functions.allowance(public_key, contract_address).call() / (
            10 ** bidding_token.functions.decimals().call()
        )

        return bool(allowance > 1e30)
