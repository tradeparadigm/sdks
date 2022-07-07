#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Anil@Opyn
# Created Date: 06/07/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------

import os

from dotenv import load_dotenv

from opyn.definitions import *
from opyn.settlement import SettlementContract
from opyn.wallet import Wallet

load_dotenv()

rpc_token = os.getenv('RPC_TOKEN')
current_chain = Chains.ROPSTEN
rpc = {Chains.ROPSTEN: os.getenv('RPC_URL')}
rpc_uri = rpc[current_chain] + rpc_token

osqth_token_address = "0xa4222f78d23593e82Aa74742d25D06720DCa4ab7"
opyn_usdc_token_address = "0x27415c30d8c87437becbd4f98474f26e712047f4"

# settlement contract with offerId only 0xF5B37514e82252E83d12DfEDf7b26d0145Ab3969
# settlement contract with offerId and bidId 0xE30193f1dE9Ae5E37e99DA868B9Cb200e7731Cf7
settlement_contract_address = "0xE30193f1dE9Ae5E37e99DA868B9Cb200e7731Cf7"
settlement_config = ContractConfig(settlement_contract_address, rpc_uri, current_chain)
settlement_contract = SettlementContract(settlement_config)

domain = Domain("OPYN BRIDGE", "1", 3, settlement_contract_address)

maker_public = os.getenv('MAKER_PubKEY')
maker_private = os.getenv('MAKER_PrivKEY')
maker_wallet = Wallet(maker_public, maker_private)

taker_public = os.getenv('TAKER_PubKEY')
taker_private = os.getenv('TAKER_PrivKEY')
taker_wallet = Wallet(taker_public, taker_private)

total_size = 10**18
min_bid_amount = total_size
min_price = 1
offerToCreate = Offer(
    osqth_token_address, opyn_usdc_token_address, min_price, min_bid_amount, total_size
)
# settlement_contract.create_offer(offerToCreate, taker_wallet)

offerId = settlement_contract.get_offer_counter()
maker_order_amount = 10**18
maker_nonce = settlement_contract.nonce(maker_wallet.public_key)
# maker_message = MessageToSign(
#     offerId=offerId,
#     bidId=1,
#     signerAddress=maker_wallet.public_key,
#     bidderAddress=maker_wallet.public_key,
#     bidToken=opyn_usdc_token_address,
#     offerToken=osqth_token_address,
#     bidAmount=maker_order_amount,
#     sellAmount=1000*10**6,
#     nonce=maker_nonce
# )
# signed_maker_order = maker_wallet.sign_bid_data(domain, maker_message)
# on_chain_signer = settlement_contract.get_bid_signer(signed_maker_order)
# print("maker_public", maker_public)
# print('on_chain_signer', on_chain_signer)
# result = settlement_contract.validate_bid(signed_maker_order)
# print(result)
# # offer_details = settlement_contract.get_offer_details(offerId)
# # print('offerDetails', offer_details)

print('offerId', offerId, type(offerId))
maker_message = TestToSign(
    offerId=offerId,
    bidId=1,
)
signed_maker_order = maker_wallet.sign_test_data(domain, maker_message)
on_chain_signer = settlement_contract.get_test_signer(signed_maker_order)
print("maker_public", maker_public)
print('on_chain_signer', on_chain_signer)
# result = settlement_contract.validate_bid(signed_maker_order)
# print(result)
