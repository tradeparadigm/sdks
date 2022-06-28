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

settlement_contract_address = "0xc2e46d84a7d454f46b2a2edb16e86fb2d28336e4"
settlement_config = ContractConfig(settlement_contract_address, rpc_uri, current_chain)
settlement_contract = SettlementContract(settlement_config)

domain = Domain("OPYN RFQ", "1", 3, settlement_contract_address)

maker_public = os.getenv('MAKER_PubKEY')
maker_private = os.getenv('MAKER_PrivKEY')
maker_wallet = Wallet(maker_public, maker_private)

taker_public = os.getenv('TAKER_PubKEY')
taker_private = os.getenv('TAKER_PrivKEY')
taker_wallet = Wallet(taker_public, taker_private)

sell_amount = 1000*10**6
offerToCreate = Offer(
    osqth_token_address,
    opyn_usdc_token_address,
    10*10**6,
    sell_amount,
    sell_amount
)
settlement_contract.create_offer(offerToCreate, taker_wallet)

offerId = settlement_contract.get_offer_counter()
maker_order_amount = 10**18
maker_nonce = settlement_contract.nonce(maker_wallet.public_key)
maker_message = MessageToSign(
    offerId=offerId,
    bidId=2,
    signerAddress=maker_public,
    bidderAddress=maker_public,
    bidToken=opyn_usdc_token_address,
    offerToken=osqth_token_address,
    bidAmount=maker_order_amount,
    sellAmount=sell_amount,
    nonce=maker_nonce
)
signed_maker_order = maker_wallet.sign_bid_data(domain, maker_message)
print('signed_maker_order', signed_maker_order)
result = settlement_contract.validate_bid(signed_maker_order)
print(result)
# offer_details = settlement_contract.get_offer_details(offerId)
# print('offerDetails', offer_details)
