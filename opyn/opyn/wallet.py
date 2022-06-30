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
from dataclasses import asdict
from opyn.encode import TypedDataEncoder
from opyn.definitions import  Domain, MessageToSign, BidData, ContractConfig
from opyn.erc20 import ERC20Contract
from opyn.utils import hex_zero_pad, get_address

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MESSAGE_TYPES = {
    "OpynRfq": [
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

    def sign_msg(self, messageHash: str) -> dict:
        """Sign a hash message using the signer object

        Args:
            messageHash (str): Message to signed in hex format with 0x prefix

        Returns:
            signature (dict): Signature split into v, r, s components
        """
        signature = self.signer.sign_msg_hash(bytes.fromhex(messageHash[2:]))

        return {
            "v": signature.v + 27, 
            "r": hex_zero_pad(hex(signature.r), 32), 
            "s": hex_zero_pad(hex(signature.s), 32)
        }

    def _sign_type_data_v4(self, domain: Domain, value: dict, types: dict) -> str:
        """Sign a hash of typed data V4 which follows EIP712 convention:
        https://eips.ethereum.org/EIPS/eip-712

        Args:
            domain (dict): Dictionary containing domain parameters including
              name, version, chainId, verifyingContract and salt (optional)
            types (dict): Dictionary of types and their fields
            value (dict): Dictionary of values for each field in types

        Raises:
            TypeError: Domain argument is not an instance of Domain class

        Returns:
            signature (dict): Signature split into v, r, s components
        """
        if not isinstance(domain, Domain):
            raise TypeError("Invalid domain parameters")

        domain_dict = {k: v for k, v in asdict(domain).items() if v is not None}

        return self.sign_msg(TypedDataEncoder._hash(domain_dict, types, value))

    def sign_bid_data(self, domain: Domain, message_to_sign: MessageToSign) -> BidData:
        """Sign a bid using _sign_type_data_v4

        Args:
            domain (dict): Dictionary containing domain parameters including
              name, version, chainId, verifyingContract and salt (optional)
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

        signature = self._sign_type_data_v4(domain, asdict(message_to_sign), MESSAGE_TYPES)
        print('signature', signature)
        
        return BidData(
            offerId=message_to_sign.offerId,
            bidId=message_to_sign.bidId,
            signerAddress=message_to_sign.signerAddress,
            bidderAddress=message_to_sign.bidderAddress,
            bidToken=message_to_sign.bidToken,
            offerToken=message_to_sign.offerToken,
            bidAmount=message_to_sign.bidAmount,
            sellAmount=message_to_sign.sellAmount,
            v=signature["v"],
            r=signature["r"],
            s=signature["s"],
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
