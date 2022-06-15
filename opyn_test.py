#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Anil@Opyn
# Created Date: 06/07/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------

from opyn.definitions import *
# from opyn.erc20 import ERC20Contract
from opyn.settlement import SettlementContract
from opyn.wallet import Wallet
from dataclasses import asdict

from dotenv import load_dotenv
import os

load_dotenv()

rpc_token = os.getenv('RPC_TOKEN')
current_chain = Chains.ROPSTEN
rpc = {
    Chains.ROPSTEN: os.getenv('RPC_URL')
}
rpc_uri = rpc[current_chain] + rpc_token

osqth_token_address = "0xa4222f78d23593e82Aa74742d25D06720DCa4ab7"
opyn_usdc_token_address = "0x27415c30d8c87437becbd4f98474f26e712047f4"

settlement_contract_address = "0x0e709c6e73dcbcb169c29e4412f905a16d5aff4e"
settlement_config = ContractConfig(settlement_contract_address, rpc_uri, current_chain)
settlement_contract = SettlementContract(settlement_config)

domain = Domain("OPYN RFQ", "1", 3, "0x0e709c6e73dcbcb169c29e4412f905a16d5aff4e")

maker_public = os.getenv('MAKER_PubKEY')
maker_private = os.getenv('MAKER_PrivKEY')
maker_wallet = Wallet(maker_public, maker_private, os.getenv('RELAYER_API'))

maker_order_amount = str(1)
maker_nonce = settlement_contract.nonce(maker_wallet.public_key)
maker_message = MessageToSign(2, maker_public, opyn_usdc_token_address, maker_order_amount, maker_nonce)
signed_maker_order = maker_wallet.sign_order_data(domain, maker_message)

taker_public = os.getenv('TAKER_PubKEY')
taker_private = os.getenv('TAKER_PrivKEY')
taker_wallet = Wallet(taker_public, taker_private, os.getenv('RELAYER_API'))

taker_order_amount = str(1)
taker_nonce = settlement_contract.nonce(taker_wallet.public_key)
taker_message = MessageToSign(1, taker_public, osqth_token_address, taker_order_amount, taker_nonce)
signed_taker_order = taker_wallet.sign_order_data(domain, taker_message)

# maker_wallet.allow_more(settlement_config, opyn_usdc_token_address, maker_order_amount)
# taker_wallet.allow_more(settlement_config, osqth_token_address, taker_order_amount)

maker_wallet.settle_trade("744", ContractConfig(settlement_contract_address, rpc_uri, current_chain), signed_maker_order)