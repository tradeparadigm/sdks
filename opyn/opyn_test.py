#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Anil@Opyn
# Created Date: 06/07/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------

import os

from dotenv import load_dotenv

from opyn.definitions import Chains, ContractConfig, Domain, MessageToSign, Offer
from opyn.settlement import SettlementContract
from opyn.wallet import Wallet

load_dotenv()

current_chain = Chains.ROPSTEN


def get_env(variable: str) -> str:
    value = os.getenv(variable)
    assert value is not None, f"Missing env variable {variable}"
    return value


rpc_token = get_env('RPC_TOKEN')
rpc_url = get_env('RPC_URL')
maker_public = get_env('MAKER_PubKEY')
maker_private = get_env('MAKER_PrivKEY')
taker_public = get_env('TAKER_PubKEY')
taker_private = get_env('TAKER_PrivKEY')

rpc_uri = rpc_url + rpc_token

osqth_token_address = "0xa4222f78d23593e82Aa74742d25D06720DCa4ab7"
opyn_usdc_token_address = "0x27415c30d8c87437becbd4f98474f26e712047f4"

settlement_contract_address = "0xc18DAA3DBE4B0F0810c8A4EeABc225713313204e"
settlement_config = ContractConfig(settlement_contract_address, rpc_uri, current_chain)
settlement_contract = SettlementContract(settlement_config)

domain = Domain("OPYN BRIDGE", "1", 3, settlement_contract_address)

maker_wallet = Wallet(maker_public, maker_private)
taker_wallet = Wallet(taker_public, taker_private)

assert maker_wallet.public_key, "Maker Public Key is None"
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
