#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Anil@Opyn
# Created Date: 06/07/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------

import os
from opyn.definitions import *
from opyn.settlement import SettlementContract
from opyn.wallet import Wallet
from dotenv import load_dotenv

load_dotenv()

rpc_token = os.getenv('RPC_TOKEN')
current_chain = Chains.ROPSTEN
rpc = {
    Chains.ROPSTEN: os.getenv('RPC_URL')
}
rpc_uri = rpc[current_chain] + rpc_token

osqth_token_address = "0xa4222f78d23593e82Aa74742d25D06720DCa4ab7"
opyn_usdc_token_address = "0x27415c30d8c87437becbd4f98474f26e712047f4"

settlement_contract_address = "0x8B5d3C00Cf5763dCF3bE16fd4045D99A2e948B0a"
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
    osqth_token_address,
    opyn_usdc_token_address,
    min_price,
    min_bid_amount,
    total_size
)
settlement_contract.create_offer(offerToCreate, taker_wallet)

offerId = settlement_contract.get_offer_counter()
maker_order_amount = 10**18
maker_nonce = int(settlement_contract.nonce(maker_wallet.public_key))
maker_message = MessageToSign(
    offerId=offerId,
    bidderAddress=maker_wallet.public_key,
    bidId=1,
    signerAddress=maker_wallet.public_key,
    bidAmount=maker_order_amount,
    offerToken=osqth_token_address,
    sellAmount=1*10**6,
    bidToken=opyn_usdc_token_address,
    nonce=maker_nonce
)
signed_maker_order = maker_wallet.sign_bid_data(domain, maker_message)
print('maker_wallet.public_key', maker_wallet.public_key)
on_chain_signer = settlement_contract.get_bid_signer(signed_maker_order)
print('on_chain_signer', on_chain_signer)
result = settlement_contract.validate_bid(signed_maker_order)
print(result)
# offer_details = settlement_contract.get_offer_details(offerId)
# print('offerDetails', offer_details)
# settlement_contract.settle_offer(offerId, signed_maker_order, taker_wallet)
