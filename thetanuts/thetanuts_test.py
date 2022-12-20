#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Pecan@Thetanuts
# Created Date: 13/10/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------

import json
import os
import time
from binascii import unhexlify
from decimal import Decimal

import eth_keys  # type: ignore
import web3
from web3.middleware import geth_poa_middleware

from thetanuts.config import Thetanuts
from thetanuts.definitions import Chains, Domain
from thetanuts.wallet import Wallet


def get_env(variable: str) -> str:
    value = os.getenv(variable)
    assert value is not None, f"Missing env variable {variable}"
    return value


current_chain = Chains.MATIC
chain_id = current_chain.value
rpc_uri = "https://polygon-rpc.com"

w3 = web3.Web3(web3.HTTPProvider(rpc_uri))
if chain_id == Chains.MATIC.value:
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)  # For MATIC chains


owner_private = "0x" + get_env('OWNER_PRVKEY')
maker_private = "0x" + get_env('MAKER_PRVKEY')
taker_private = "0x" + get_env('TAKER_PRVKEY')

owner_public = eth_keys.keys.private_key_to_public_key(
    eth_keys.datatypes.PrivateKey(unhexlify(owner_private[2:]))
).to_checksum_address()
maker_public = eth_keys.keys.private_key_to_public_key(
    eth_keys.datatypes.PrivateKey(unhexlify(maker_private[2:]))
).to_checksum_address()
taker_public = eth_keys.keys.private_key_to_public_key(
    eth_keys.datatypes.PrivateKey(unhexlify(taker_private[2:]))
).to_checksum_address()

# tweth_token_address = "0xd9F0446AedadCf16A12692E02FA26C617FA4D217"
# Above address to be picked up from the vault contract
oToken = vault_contract_address = "0x4a3c6DA195506ADC87D984C5B429708c8Ddd4237"
contract_address = bridge_contract_address = "0x3a9212E96EEeBEADDCe647E298C0610BEB071eE3"

bridgeContract = w3.eth.contract(
    w3.toChecksumAddress(bridge_contract_address),
    abi=json.load(open("thetanuts/abis/ParadigmBridge.json", "r")),
)

domain = Domain("Thetanuts", "1.0", 137, bridge_contract_address)

owner_wallet = Wallet(owner_public, owner_private)
maker_wallet = Wallet(maker_public, maker_private)
taker_wallet = Wallet(taker_public, taker_private)

assert owner_wallet.public_key, "Owner Public Key is None"
assert maker_wallet.public_key, "Maker Public Key is None"
assert taker_wallet.public_key, "Taker Public Key is None"

# Maker gets information on asset

vault = w3.eth.contract(
    w3.toChecksumAddress(vault_contract_address),
    abi=json.load(open("thetanuts/abis/Vault.json", "r")),
)

tweth_token_address = vault.functions.COLLAT().call()

collat = w3.eth.contract(
    w3.toChecksumAddress(tweth_token_address),
    abi=json.load(open("thetanuts/abis/ERC20.json", "r")),
)

COLLAT_DECIMALS = Decimal(10 ** collat.functions.decimals().call())
BRIDGE_DECIMALS = Decimal(
    "1e6"
)  # Strike price and number of contracts returned from the ParadigmBridge is multiplied by 1e6


# Maker sets price per contract

pricePerContract = "0.002"

# Start new round (Performed by Bridge/Vault owner account)
thetanuts = Thetanuts()
thetanuts.create_offer(
    oToken=vault_contract_address,
    contract_address=bridge_contract_address,
    chain_id=current_chain.value,
    rpc_uri=rpc_uri,
    bidding_token=tweth_token_address,
    min_price=0,
    min_bid_size=0,
    offer_amount=0,
    public_key=owner_public,
    private_key=owner_private,
)

# Wait for RPC to be ready
while True:
    if bridgeContract.functions.getAuctionDetails(oToken).call()[3] == 0:
        print("Waiting for RPC to be ready...")
        time.sleep(5)
    else:
        break


# Maker checks contract for auction info

vaultInfo = thetanuts.get_otoken_details(
    contract_address=bridge_contract_address,
    oToken=vault_contract_address,
    chain_id=current_chain.value,
    rpc_uri=rpc_uri,
)
print("Vault info:", vaultInfo)

# Maker checks contract for offer info
offer = thetanuts.get_offer_details(
    contract_address=bridge_contract_address,
    offer_id=int(vault_contract_address, 16),
    chain_id=current_chain.value,
    rpc_uri=rpc_uri,
)
print("Current offer:", offer)

# Maker signs bid for submission

signed_bid = thetanuts.sign_bid(
    contract_address=bridge_contract_address,
    chain_id=current_chain.value,
    rpc_uri=rpc_uri,
    swap_id=int(vault_contract_address, 16),
    sell_amount=int(
        Decimal(offer["availableSize"])
        * Decimal(pricePerContract)
        * COLLAT_DECIMALS
        / BRIDGE_DECIMALS
    ),
    buy_amount=int(offer["availableSize"]),
    referrer="0x" + "0" * 40,
    signer_wallet=maker_public,
    public_key=maker_public,
    private_key=maker_private,
    nonce=vaultInfo["expiryTimestamp"],
)
print("Signed bid:", signed_bid)

# Validate bid through ParadigmBridge contract

print("Validating bid via assert")
if (
    thetanuts.validate_bid(
        contract_address=bridge_contract_address,
        chain_id=current_chain.value,
        rpc_uri=rpc_uri,
        swap_id=int(vault_contract_address, 16),
        nonce=vaultInfo["expiryTimestamp"],
        signer_wallet=maker_public,
        sell_amount=int(
            Decimal(offer["availableSize"])
            * Decimal(pricePerContract)
            * COLLAT_DECIMALS
            / BRIDGE_DECIMALS
        ),
        buy_amount=int(Decimal(offer["availableSize"]) * COLLAT_DECIMALS / BRIDGE_DECIMALS),
        referrer="0x" + "0" * 40,
        signature=signed_bid,
    )["errors"]
    is False
):
    print("Bid validated")

# Paradigm validates allowance

print("Verifying allowance via assert")
allowance = thetanuts.verify_allowance(
    contract_address=bridge_contract_address,
    chain_id=current_chain.value,
    rpc_uri=rpc_uri,
    public_key=maker_public,
    token_address=offer["biddingToken"],
)
if (
    thetanuts.verify_allowance(
        contract_address=bridge_contract_address,
        chain_id=current_chain.value,
        rpc_uri=rpc_uri,
        public_key=maker_public,
        token_address=offer["biddingToken"],
    )
    is True
):
    print("Allowance verified")

# Contract/ParadigmBridge owner transmits sign_bid to ParadigmBridge

tx = bridgeContract.functions.pullAssetsAndStartRound(
    vault_contract_address,
    [vaultInfo["strikePrice"]],
    int(
        Decimal(offer["availableSize"])
        * Decimal(pricePerContract)
        * COLLAT_DECIMALS
        / BRIDGE_DECIMALS
    ),
    int(Decimal(offer["availableSize"]) * COLLAT_DECIMALS / BRIDGE_DECIMALS),
    int(vaultInfo["expiryTimestamp"]),
    maker_public,
    signed_bid,
).build_transaction({'nonce': w3.eth.get_transaction_count(owner_public), 'from': owner_public})
signedTx = w3.eth.send_raw_transaction(
    w3.eth.account.sign_transaction(tx, owner_private).rawTransaction
)
print("Sent OWNER transaction for pulling assets from MAKER to start new round", signedTx.hex())
w3.eth.wait_for_transaction_receipt(signedTx)
