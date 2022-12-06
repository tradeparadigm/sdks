#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Pecan@Thetanuts
# Created Date: 13/10/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------

import os
from binascii import unhexlify

import eth_keys
import web3
from web3.middleware import geth_poa_middleware

from thetanuts.definitions import Bid, Chains, ContractConfig, Domain, Offer, SignedBid
from thetanuts.wallet import Wallet

current_chain = Chains.MATIC


def get_env(variable: str) -> str:
    value = os.getenv(variable)
    assert value is not None, f"Missing env variable {variable}"
    return value


rpc_uri = "https://polygon-rpc.com"

owner_private = get_env('OWNER_PRVKEY')
maker_private = get_env('MAKER_PRVKEY')
taker_private = get_env('TAKER_PRVKEY')

owner_public = eth_keys.keys.private_key_to_public_key(
    eth_keys.datatypes.PrivateKey(unhexlify(owner_private))
).to_checksum_address()
maker_public = eth_keys.keys.private_key_to_public_key(
    eth_keys.datatypes.PrivateKey(unhexlify(maker_private))
).to_checksum_address()
taker_public = eth_keys.keys.private_key_to_public_key(
    eth_keys.datatypes.PrivateKey(unhexlify(taker_private))
).to_checksum_address()

tweth_token_address = "0xa4222f78d23593e82Aa74742d25D06720DCa4ab7"
vault_contract_address = "0x4a3c6DA195506ADC87D984C5B429708c8Ddd4237"
bridge_contract_address = "0x1d1a9ff640F58740F2c240C460BfE193CcE395d1"
domain = Domain("Thetanuts", "1.0", 137, bridge_contract_address)

owner_wallet = Wallet(owner_public, "0x" + owner_private)
maker_wallet = Wallet(maker_public, "0x" + maker_private)
taker_wallet = Wallet(taker_public, "0x" + taker_private)

assert maker_wallet.public_key, "Maker Public Key is None"

# Start new round

thetanuts = TemplateSDKConfig()


total_size = 10**18
min_bid_amount = total_size
min_price = 1
offerToCreate = Offer(
    osqth_token_address, opyn_usdc_token_address, min_price, min_bid_amount, total_size
)
settlement_contract.create_offer(offerToCreate, taker_wallet)

offerId = settlement_contract.get_offer_counter()
maker_order_amount = 10**18
maker_nonce = settlement_contract.nonce(maker_wallet.public_key)
maker_message = MessageToSign(
    offerId=offerId,
    bidId=1,
    signerAddress=maker_wallet.public_key,
    bidderAddress=maker_wallet.public_key,
    bidToken=opyn_usdc_token_address,
    offerToken=osqth_token_address,
    bidAmount=maker_order_amount,
    sellAmount=1000 * 10**6,
    nonce=maker_nonce,
)
signed_maker_order = maker_wallet.sign_bid_data(domain, maker_message)
on_chain_signer = settlement_contract.get_bid_signer(signed_maker_order)
print("maker_public", maker_public)
print('on_chain_signer', on_chain_signer)
result = settlement_contract.validate_bid(signed_maker_order)
print(result)
offer_details = settlement_contract.get_offer_details(offerId)
print('offerDetails', offer_details)
maker_wallet.allow_more(settlement_config, osqth_token_address, 1 * 10**18)
