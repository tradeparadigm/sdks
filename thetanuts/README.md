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

## Install the SDK

    pip3 install /tmp/code

## Run thetanuts test for a end-to-end flow

    cd thetanuts
    python3 thetanuts_test.py

## Usage

### To begin, define the interaction chain

    import sdk_commons
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

    vaultInfo = thetanuts.get_otoken_details(
      contract_address=bridge_contract_address, 
      oToken=vault_contract_address, 
      chain_id=current_chain.value, 
      rpc_uri=rpc_uri
    )
    print("Vault info:", vaultInfo)

#### Secondly, check for offer info

    offer = thetanuts.get_offer_details(
      contract_address=bridge_contract_address, 
      offer_id=int(vault_contract_address,16), 
      chain_id=current_chain.value, 
      rpc_uri=rpc_uri
    )
    print("Current offer:", offer)

#### Collect token decimals for proper scaling

    vault = w3.eth.contract(
        w3.toChecksumAddress(vault_contract_address),
        abi=sdk_commons.helpers.get_abi("Thetanuts_Vault"),
    )

    tweth_token_address = vault.functions.COLLAT().call()

    collat = w3.eth.contract(
        w3.toChecksumAddress(tweth_token_address),
        abi=sdk_commons.helpers.get_abi("ERC20"),
    )


    COLLAT_DECIMALS = Decimal(10 ** collat.functions.decimals().call())
    BRIDGE_DECIMALS = Decimal(
        "1e6"
    )  # Strike price and number of contracts returned from the ParadigmBridge is multiplied by 1e6

#### Construct bid

    pricePerContract = "0.002"

    #As there are no partials, the full size must be taken, hence buy_amount accepted will only be full offer size

    sell_bid = offer["availableSize"] * pricePerContract # Amount to bid for the entire size

    # Set keys
    maker_public = "..."
    maker_private = "..."

    signed_bid = thetanuts.sign_bid(
        contract_address=bridge_contract_address, 
        chain_id=current_chain.value, 
        rpc_uri=rpc_uri, 
        swap_id = int(vault_contract_address,16), 
        sell_amount=sell_bid_amount * COLLAT_DECIMALS / BRIDGE_DECIMALS, 
        buy_amount=offer["availableSize"] * COLLAT_DECIMALS / BRIDGE_DECIMALS, 
        referrer="0x"+"0"*40, 
        signer_wallet=maker_public, 
        public_key=maker_public, 
        private_key=maker_private,
        nonce=vaultInfo["expiryTimestamp"]
    )

#### Validate Bid Onchain

The bid will be submitted for verification to the smart contract

    result = thetanuts.validate_bid(
      contract_address=bridge_contract_address, 
      chain_id=current_chain.value,
      rpc_uri=rpc_uri, 
      swap_id = int(vault_contract_address,16), 
      nonce=vaultInfo["expiryTimestamp"], 
      signer_wallet=maker_public, 
      sell_amount=offer["availableSize"] * pricePerContract * COLLAT_DECIMALS / BRIDGE_DECIMALS,
      buy_amount=offer["availableSize"] * COLLAT_DECIMALS / BRIDGE_DECIMALS, 
      referrer="0x"+"0"*40, 
      signature=signed_bid
    )

    print(result)
    # If the Bid is valid, we see
    # {'errors': False}

#### Validate Wallet

    allowance = thetanuts.verify_allowance(contract_address=bridge_contract_address, chain_id=current_chain.value, rpc_uri=rpc_uri, public_key=maker_public, token_address=offer["biddingToken"])

    assert allowance

    # Returns True if allowance > 1e30
