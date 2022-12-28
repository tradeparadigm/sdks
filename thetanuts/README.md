# Thetanuts Finance SDK

Python SDK to interact with Thetanuts Finance auctions on Paradigm

## Setup to run sample thetanuts test script

Open a container with python
$ docker run -it --rm \
    -v $(pwd):/tmp/code -w /tmp/code \
    -p 8888:8888 \
    python:3.10 \
    bash

## Export keys into environment

    export OWNER_PRVKEY="..."
    export TAKER_PRVKEY="..."
    export MAKER_PRVKEY="..."

## Install the libraries

    pip3 install eth_keys web3==5.31.3

## Install the sdk_commons

    pip3 install /tmp/code/sdk_commons

## Run thetanuts test for a end-to-end flow

    cd thetanuts
    python3 thetanuts_test.py

## Usage

### To begin, define the interaction chain

    from thetanuts.definitions import Bid, Domain, ContractConfig, Offer, SignedBid, Chains
    from thetanuts.wallet import Wallet
    from thetanuts.config import Thetanuts
    
    current_chain = Chains.MATIC
    chain_id = current_chain.value
    rpc_uri = "https://polygon-rpc.com"

## Interface to Thetanuts

    thetanuts = Thetanuts()

### Signing Bids

#### First check for auction information for a given contract

    oToken = vault_contract_address = "0x4a3c6DA195506ADC87D984C5B429708c8Ddd4237"
    contract_address = bridge_contract_address = "0x3a9212E96EEeBEADDCe647E298C0610BEB071eE3"

    vaultInfo = thetanuts.get_otoken_details(contract_address=bridge_contract_address, oToken=vault_contract_address, chain_id=current_chain.value, rpc_uri=rpc_uri)
    print("Vault info:", vaultInfo)

#### Secondly, check for offer info

    offer = thetanuts.get_offer_details(contract_address=bridge_contract_address, offer_id=int(vault_contract_address,16), chain_id=current_chain.value, rpc_uri=rpc_uri)
    print("Current offer:", offer)

#### Construct bid

    #As there are no partials, the full size must be taken, hence buy_amount accepted will only be full offer size

    sell_bid = offer["availableSize"] * Decimal("0.002") # Amount to bid for the entire size

    # Set keys
    maker_public = "..."
    maker_private = "..."

    signed_bid = thetanuts.sign_bid(
        contract_address=bridge_contract_address, 
        chain_id=current_chain.value, 
        rpc_uri=rpc_uri, 
        swap_id = int(vault_contract_address,16), 
        sell_amount=sell_bid_amount, 
        buy_amount=offer["availableSize"], 
        referrer="0x"+"0"*40, 
        signer_wallet=maker_public, 
        public_key=maker_public, 
        private_key=maker_private,
        nonce=vaultInfo["expiryTimestamp"]
    )

#### Validate Bid Onchain

The bid will be submitted for verification to the smart contract

    result = thetanuts.validate_bid(contract_address=bridge_contract_address, chain_id=current_chain.value, rpc_uri=rpc_uri, swap_id = int(vault_contract_address,16),  nonce=vaultInfo["expiryTimestamp"], signer_wallet=maker_public, sell_amount=offer["availableSize"]*Decimal("0.002"), buy_amount=offer["availableSize"], referrer="0x"+"0"*40, signature=signed_bid)

    print(result)
    # If the Bid is valid, we see
    # {'errors': False}

#### Validate Wallet

    allowance = thetanuts.verify_allowance(contract_address=bridge_contract_address, chain_id=current_chain.value, rpc_uri=rpc_uri, public_key=maker_public, token_address=offer["biddingToken"])

    assert True == thetanuts.verify_allowance(contract_address=bridge_contract_address, chain_id=current_chain.value, rpc_uri=rpc_uri, public_key=maker_public, token_address=offer["biddingToken"])

    # Returns True if allowance > 1e30
