#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Anil@Opyn
# Created Date: 06/07/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------

from opyn.definitions import Domain, MessageToSign, Chains, ContractConfig
from opyn.erc20 import ERC20Contract
from opyn.settlement import Settlement
from opyn.contract import ContractConnection
from opyn.wallet import Wallet

import os

rpc_token = os.getenv('RPC_TOKEN')
osqth_token_address = "0xa4222f78d23593e82Aa74742d25D06720DCa4ab7"
current_chain = Chains.ROPSTEN
rpc = {
    Chains.ROPSTEN: "https://eth-ropsten.alchemyapi.io/v2/"
}
rpc_uri = rpc[current_chain] + rpc_token

token_config = ContractConfig(
            address=osqth_token_address,
            rpc_uri=rpc_uri,
            chain_id=current_chain,
        )
osqth_token = ERC20Contract(token_config)

public_key = "0xf119423b59f58A0a45C89b086f079aA9fFFbc3B1"
balance = osqth_token.get_balance(public_key)
print(f"oSQTH balance of address {public_key} is {balance}")

domain = Domain("OPYN", 3, "0x529189A6684C8deA7D01d2d1329c01E38Fefb314", 1)

taker_public = "0x917e2bF1484E94935C8664C8dC2B768073cceFcB"
taker_private = os.getenv('TAKER_PKEY')

taker_wallet  = Wallet(taker_public, taker_private)
taker_message = MessageToSign(1, taker_public, osqth_token_address, 2, 1 )
signed_taker_order = taker_wallet.sign_order_data(domain, taker_message)

maker_public = "0x591540D17259838e73323892B4AefF11244B2DF4"
maker_private = os.getenv('MAKER_PKEY')
maker_wallet = Wallet(maker_public, maker_private)
maker_message = MessageToSign(1, maker_public, osqth_token_address, 2 , 1)
signed_maker_order = maker_wallet.sign_order_data(domain, maker_message)

settlement_contract_address = "0x529189A6684C8deA7D01d2d1329c01E38Fefb314"

settlement_config = ContractConfig(settlement_contract_address, rpc_uri, current_chain)

settlement_contract = Settlement(settlement_config)
settlement_contract.settleRfq(signed_taker_order,signed_maker_order)