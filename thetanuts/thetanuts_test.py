#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# Created By: Pecan@Thetanuts
# Created Date: 13/10/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------

import os
import time
from binascii import unhexlify
from decimal import Decimal

import eth_keys  # type: ignore
import web3
from web3.middleware import geth_poa_middleware

import sdk_commons
from sdk_commons.chains import Chains
from thetanuts.config import Thetanuts
from thetanuts.wallet import Wallet


def get_env(variable: str) -> str:
    value = os.getenv(variable)
    assert value is not None, f"Missing env variable {variable}"
    return value


current_chain = Chains.MATIC
rpc_uri = "https://polygon-rpc.com"

w3 = web3.Web3(web3.HTTPProvider(rpc_uri))
if current_chain == Chains.MATIC:
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
contract_address = bridge_contract_address = "0x16d56571653aEb3a0a666d6BBe2EC5196E7078ff"


bridgeContract = w3.eth.contract(
    w3.toChecksumAddress(bridge_contract_address),
    abi=sdk_commons.helpers.get_abi("Thetanuts_ParadigmBridge"),
)

vault_id = bridgeContract.functions.vaultIndexToAddress(vault_contract_address).call()

owner_wallet = Wallet(owner_public, owner_private)
maker_wallet = Wallet(maker_public, maker_private)
taker_wallet = Wallet(taker_public, taker_private)

assert owner_wallet.public_key, "Owner Public Key is None"
assert maker_wallet.public_key, "Maker Public Key is None"
assert taker_wallet.public_key, "Taker Public Key is None"

# Maker gets information on asset

vault = w3.eth.contract(
    w3.toChecksumAddress(vault_contract_address),
    abi=sdk_commons.helpers.get_abi("Thetanuts_Vault"),
)

tweth_token_address = vault.functions.COLLAT().call()
vault_epoch = vault.functions.epoch().call() + 1

collat = w3.eth.contract(
    w3.toChecksumAddress(tweth_token_address),
    abi=sdk_commons.helpers.get_abi("ERC20"),
)

COLLAT_DECIMALS = Decimal(10 ** collat.functions.decimals().call())
BRIDGE_DECIMALS = Decimal("1e6")
PARADIGM_DECIMALS = Decimal("1e8")

# Maker sets price per contract
pricePerContract = "0.002"

# Start new round (Performed by Bridge/Vault owner account)
thetanuts = Thetanuts()

thetanuts.create_offer(
    oToken=vault_contract_address,
    contract_address=bridge_contract_address,
    chain_id=current_chain,
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
    contract_address=vault_contract_address,
    swap_contract_address=bridge_contract_address,
    chain_id=current_chain,
    rpc_uri=rpc_uri,
)
print("Vault info:", vaultInfo)

# Maker checks contract for offer info
offer = thetanuts.get_offer_details(
    contract_address=bridge_contract_address,
    offer_id=(vault_id << 16) + vault_epoch,
    chain_id=current_chain,
    rpc_uri=rpc_uri,
)
print("Current offer:", offer)

# Maker signs bid for submission

signed_bid = thetanuts.sign_bid(
    contract_address=vault_contract_address,
    chain_id=current_chain,
    rpc_uri=rpc_uri,
    swap_id=(vault_id << 16) + vault_epoch,
    sell_amount=int(
        Decimal(offer["availableSize"])
        * Decimal(pricePerContract)
        * COLLAT_DECIMALS
        / PARADIGM_DECIMALS
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

print("Validating bid by checking validate_bid(..) returns {'errors': False} ")
if (
    thetanuts.validate_bid(
        contract_address=bridge_contract_address,
        chain_id=current_chain,
        rpc_uri=rpc_uri,
        swap_id=(vault_id << 16) + vault_epoch,
        nonce=vaultInfo["expiryTimestamp"],
        signer_wallet=maker_public,
        sell_amount=int(
            Decimal(offer["availableSize"])
            * Decimal(pricePerContract)
            * COLLAT_DECIMALS
            / PARADIGM_DECIMALS
        ),
        buy_amount=int(Decimal(offer["availableSize"]) * COLLAT_DECIMALS / PARADIGM_DECIMALS),
        referrer="0x" + "0" * 40,
        signature=signed_bid,
    )["errors"]
    is False
):
    print(" -> Bid validated")
else:
    print(" -> Bid validation failed!")

# Paradigm validates allowance

print("Verifying allowance by ensuring verify_allowance returns True")
if (
    thetanuts.verify_allowance(
        contract_address=bridge_contract_address,
        chain_id=current_chain,
        rpc_uri=rpc_uri,
        public_key=maker_public,
        token_address=offer["biddingToken"],
    )
    is True
):
    print(" -> Allowance verified")
else:
    print(" -> Allowance not set!")

# Contract/ParadigmBridge owner transmits sign_bid to ParadigmBridge

tx = bridgeContract.functions.pullAssetsAndStartRound(
    vault_contract_address,
    [int(vaultInfo["strikePrice"] * BRIDGE_DECIMALS / PARADIGM_DECIMALS)],
    int(
        Decimal(offer["availableSize"])
        * Decimal(pricePerContract)
        * COLLAT_DECIMALS
        / PARADIGM_DECIMALS
    ),
    int(Decimal(offer["availableSize"]) * COLLAT_DECIMALS / PARADIGM_DECIMALS),
    int(vaultInfo["expiryTimestamp"]),
    maker_public,
    signed_bid,
).build_transaction({'nonce': w3.eth.get_transaction_count(owner_public), 'from': owner_public})
signedTx = w3.eth.send_raw_transaction(
    w3.eth.account.sign_transaction(tx, owner_private).rawTransaction
)
print("Sent OWNER transaction for pulling assets from MAKER to start new round", signedTx.hex())
w3.eth.wait_for_transaction_receipt(signedTx)

# Repeat the above for the put vault
print("Perform test for PUT vault - using tUSDC")

vault_contract_address = "0x95f907d6Dcd0ea1F4F53E1e63c72Ed1E1471FEa7"
vault_id = bridgeContract.functions.vaultIndexToAddress(vault_contract_address).call()
tusdc_token_address = "0xcEAfECFf7F1923F72e5506c3FB726abB890C4391"
pricePerContract = "10"
COLLAT_DECIMALS = Decimal("1e6")  # TUSDC resolution

# Start new round (Performed by Bridge/Vault owner account)
thetanuts.create_offer(
    oToken=vault_contract_address,
    contract_address=bridge_contract_address,
    chain_id=current_chain,
    rpc_uri=rpc_uri,
    bidding_token=tusdc_token_address,
    min_price=0,
    min_bid_size=0,
    offer_amount=0,
    public_key=owner_public,
    private_key=owner_private,
)

# Wait for RPC to be ready
while True:
    if bridgeContract.functions.getAuctionDetails(vault_contract_address).call()[3] == 0:
        print("Waiting for RPC to be ready...")
        time.sleep(5)
    else:
        break

# Maker checks contract for auction info

vaultInfo = thetanuts.get_otoken_details(
    contract_address=vault_contract_address,
    swap_contract_address=bridge_contract_address,
    chain_id=current_chain,
    rpc_uri=rpc_uri,
)
print("Vault info:", vaultInfo)

# Maker checks contract for offer info
offer = thetanuts.get_offer_details(
    contract_address=bridge_contract_address,
    offer_id=(vault_id << 16) + vault_epoch,
    chain_id=current_chain,
    rpc_uri=rpc_uri,
)
print("Current offer:", offer)

# Maker signs bid for submission

signed_bid = thetanuts.sign_bid(
    contract_address=vault_contract_address,
    chain_id=current_chain,
    rpc_uri=rpc_uri,
    swap_id=(vault_id << 16) + vault_epoch,
    sell_amount=int(
        Decimal(offer["availableSize"])
        / PARADIGM_DECIMALS
        * Decimal(pricePerContract)
        * COLLAT_DECIMALS
    ),
    buy_amount=int(Decimal(offer["availableSize"]) * BRIDGE_DECIMALS / PARADIGM_DECIMALS),
    referrer="0x" + "0" * 40,
    signer_wallet=maker_public,
    public_key=maker_public,
    private_key=maker_private,
    nonce=vaultInfo["expiryTimestamp"],
)
print("Signed bid:", signed_bid)

# Validate bid through ParadigmBridge contract

print("Validating bid by checking validate_bid(..) returns {'errors': False} ")
if (
    thetanuts.validate_bid(
        contract_address=bridge_contract_address,
        chain_id=current_chain,
        rpc_uri=rpc_uri,
        swap_id=(vault_id << 16) + vault_epoch,
        nonce=vaultInfo["expiryTimestamp"],
        signer_wallet=maker_public,
        sell_amount=int(
            Decimal(offer["availableSize"])
            / PARADIGM_DECIMALS
            * Decimal(pricePerContract)
            * COLLAT_DECIMALS
        ),
        buy_amount=int(Decimal(offer["availableSize"]) * BRIDGE_DECIMALS / PARADIGM_DECIMALS),
        referrer="0x" + "0" * 40,
        signature=signed_bid,
    )["errors"]
    is False
):
    print(" -> Bid validated")
else:
    print(" -> Bid validation failed!")

# Paradigm validates allowance

print("Verifying allowance by ensuring verify_allowance returns True")
if (
    thetanuts.verify_allowance(
        contract_address=bridge_contract_address,
        chain_id=current_chain,
        rpc_uri=rpc_uri,
        public_key=maker_public,
        token_address=offer["biddingToken"],
    )
    is True
):
    print(" -> Allowance verified")
else:
    print(" -> Allowance not set!")

# Contract/ParadigmBridge owner transmits sign_bid to ParadigmBridge

tx = bridgeContract.functions.pullAssetsAndStartRound(
    vault_contract_address,
    [int(vaultInfo["strikePrice"] * BRIDGE_DECIMALS / PARADIGM_DECIMALS)],
    int(
        Decimal(offer["availableSize"])
        / PARADIGM_DECIMALS
        * Decimal(pricePerContract)
        * COLLAT_DECIMALS
    ),
    int(
        Decimal(offer["availableSize"])
        * BRIDGE_DECIMALS
        / PARADIGM_DECIMALS
        * (vaultInfo["strikePrice"])
        / PARADIGM_DECIMALS
    ),
    int(vaultInfo["expiryTimestamp"]),
    maker_public,
    signed_bid,
).build_transaction({'nonce': w3.eth.get_transaction_count(owner_public), 'from': owner_public})
signedTx = w3.eth.send_raw_transaction(
    w3.eth.account.sign_transaction(tx, owner_private).rawTransaction
)
print("Sent OWNER transaction for pulling assets from MAKER to start new round", signedTx.hex())
w3.eth.wait_for_transaction_receipt(signedTx)
