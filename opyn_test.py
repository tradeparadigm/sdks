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

settlement_contract_address = "0x73834097f5e7c8a8b2465c80a8362d8737d8c8cd"
settlement_config = ContractConfig(settlement_contract_address, rpc_uri, current_chain)
settlement_contract = SettlementContract(settlement_config)

domain = Domain("OPYN RFQ", "1", 3, "0x73834097f5e7c8a8b2465c80a8362d8737d8c8cd")

maker_public = os.getenv('MAKER_PubKEY')
maker_private = os.getenv('MAKER_PrivKEY')
maker_wallet = Wallet(maker_public, maker_private, os.getenv('RELAYER_API'), os.getenv('RELAYER_TOKEN'))

taker_public = os.getenv('TAKER_PubKEY')
taker_private = os.getenv('TAKER_PrivKEY')
taker_wallet = Wallet(taker_public, taker_private, os.getenv('RELAYER_API'), os.getenv('RELAYER_TOKEN'))

sell_amount = 1e18
offerToCreate = Offer(
    osqth_token_address,
    opyn_usdc_token_address,
    str(10e6),
    sell_amount,
    sell_amount
)

# settlement_contract.create_offer(offerToCreate, taker_wallet)
offerId = settlement_contract.get_offer_counter()

maker_order_amount = str(1)

maker_nonce = settlement_contract.nonce(maker_wallet.public_key)
maker_message = MessageToSign(offerId, 2, maker_public, maker_public, opyn_usdc_token_address, osqth_token_address, maker_order_amount, sell_amount, maker_nonce)
signed_maker_order = maker_wallet.sign_order_data(domain, maker_message)
print('signed_maker_order', signed_maker_order)