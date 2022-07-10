#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Anil@Opyn
# Created Date: 06/08/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module for wallet utilities """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import eth_keys
from opyn.definitions import  Domain, MessageToSign, BidData, ContractConfig
from opyn.erc20 import ERC20Contract
from opyn.utils import get_address
from web3 import Web3
from py_eth_sig_utils.signing import sign_typed_data

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
# "OpynRfq(uint256 offerId, uint256 bidId, address signerAddress, address bidderAddress, address bidToken, address offerToken, uint256 bidAmount, uint256 sellAmount, uint256 nonce)"
MESSAGE_TYPES = {
    "RFQ": [
        {"name": "offerId", "type": "uint256"},
        {"name": "bidId", "type": "uint256"},
        {"name": "signerAddress", "type": "address"},
        {"name": "bidderAddress", "type": "address"},
        {"name": "bidToken", "type": "address"},
        {"name": "offerToken", "type": "address"},
        {"name": "bidAmount", "type": "uint256"},
        {"name": "sellAmount", "type": "uint256"},
        {"name": "nonce", "type": "uint256"}
    ]
}
TEST_TYPES = {
    "TEST": [
        {"name": "offerId", "type": "uint256"},
        {"name": "bidId", "type": "uint256"},
    ]
}

MIN_ALLOWANCE = 100000000


# ---------------------------------------------------------------------------
# Wallet Instance
# ---------------------------------------------------------------------------
class Wallet:
    """
    Object to generate bid signature

    Args:
        public_key (str): Public key of the user in hex format with 0x prefix
        private_key (str): Private key of the user in hex format with 0x prefix

    Attributes:
        signer (object): Instance of signer to generate signature
    """

    def __init__(self, public_key: str = None, private_key: str = None):
        if not private_key and not public_key:
            raise ValueError("Can't instanciate a Wallet without a public or private key")

        self.private_key = private_key
        self.public_key = public_key

        if self.private_key:
            self.signer = eth_keys.keys.PrivateKey(bytes.fromhex(self.private_key[2:]))
            if not self.public_key:
                self.public_key = get_address(self.signer.public_key.to_address())

    def sign_bid_data(self, domain: Domain, message_to_sign: MessageToSign) -> BidData:
        """Sign a bid using py_eth_sig_utils

        Args:
            domain (dict): Dictionary containing domain parameters including
              name, version, chainId, verifyingContract
            message_to_sign (MessageToSign): Unsigned Order Data

        Raises:
            TypeError: message_to_sign argument is not an instance of MessageToSign class

        Returns:
            signedBid (dict): Bid combined with the generated signature
        """
        if not isinstance(message_to_sign, MessageToSign):
            raise TypeError("Invalid message_to_sign(MessageToSign)")

        if not self.private_key:
            raise ValueError("Unable to sign. Create the Wallet with the private key argument.")

        message_to_sign.signerAddress = get_address(message_to_sign.signerAddress)
        message_to_sign.bidderAddress = get_address(message_to_sign.bidderAddress)
        message_to_sign.bidToken = get_address(message_to_sign.bidToken)
        message_to_sign.offerToken = get_address(message_to_sign.offerToken)

        if message_to_sign.signerAddress != self.public_key:
            raise ValueError("Signer wallet address mismatch")

        data = {
            "types": {
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                    {"name": "chainId", "type": "uint256"},
                    {"name": "verifyingContract", "type": "address"},
                ],
                "RFQ": [
                    {"name": "offerId", "type": "uint256"},
                    {"name": "bidId", "type": "uint256"},
                    {"name": "signerAddress", "type": "address"},
                    {"name": "bidderAddress", "type": "address"},
                    {"name": "bidToken", "type": "address"},
                    {"name": "offerToken", "type": "address"},
                    {"name": "bidAmount", "type": "uint256"},
                    {"name": "sellAmount", "type": "uint256"},
                    {"name": "nonce", "type": "uint256"},
                ],
            },
            "domain": {
                "name": domain.name,
                "version": domain.version,
                "chainId": domain.chainId,
                "verifyingContract": domain.verifyingContract,
            },
            "primaryType": "RFQ",
            "message": {
                "offerId": message_to_sign.offerId,
                "bidId": message_to_sign.bidId,
                "signerAddress": message_to_sign.signerAddress,
                "bidderAddress": message_to_sign.bidderAddress,
                "bidToken": message_to_sign.bidToken,
                "offerToken": message_to_sign.offerToken,
                "bidAmount": message_to_sign.bidAmount,
                "sellAmount": message_to_sign.sellAmount,
                "nonce": message_to_sign.nonce,
            },
        }
        signature = sign_typed_data(data, Web3.toBytes(hexstr=self.private_key))

        return BidData(
            offerId=message_to_sign.offerId,
            bidId=message_to_sign.bidId,
            signerAddress=message_to_sign.signerAddress,
            bidderAddress=message_to_sign.bidderAddress,
            bidToken=message_to_sign.bidToken,
            offerToken=message_to_sign.offerToken,
            bidAmount=message_to_sign.bidAmount,
            sellAmount=message_to_sign.sellAmount,
            v=signature[0],
            r=Web3.toHex(signature[1].to_bytes(32, 'big')),
            s=Web3.toHex(signature[2].to_bytes(32, 'big'))
        )

    def verify_allowance(self, settlement_config: ContractConfig, token_address: str) -> bool:
        """Verify wallet's allowance for a given token

        Args:
            config (ContractConfig): Configuration to setup the Swap Contract
            token_address (str): Address of token

        Returns:
            verified (bool): True if wallet has sufficient allowance
        """
        token_config = ContractConfig(
            address=token_address,
            rpc_uri=settlement_config.rpc_uri,
            chain_id=settlement_config.chain_id,
        )
        token = ERC20Contract(token_config)

        allowance = (
            token.get_allowance(self.public_key, settlement_config.address)
            / token.decimals
        )

        return allowance > MIN_ALLOWANCE

    def allow_more(self, settlement_config: ContractConfig, token_address: str, amount: str): 
        """Increase settlement contract allowance

        Args:
            settlement_config (ContractConfig): Configuration to setup the Settlement contract
            token_address (str): Address of token to increase allowance of
            amount (str): Amount to increase allowance to
        """
        token_config = ContractConfig(
            address=token_address,
            rpc_uri=settlement_config.rpc_uri,
            chain_id=settlement_config.chain_id,
        )
        token = ERC20Contract(token_config)

        token.approve(self.public_key, self.private_key, settlement_config.address, amount)
