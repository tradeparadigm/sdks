# Thetanuts Finance SDK

Python SDK to interact with Thetanuts Finance auctions on Paradigm

## Usage

To begin, define your domain of interaction

    from thetanuts.definitions import Chains, Domain
    from thetanuts import Thetanuts
    
    # Define the following variables:
	current_chain = Chains.MATIC

	rpc = {
	      Chains.MATIC: "https://polygon-rpc.com", 
	      Chains.ETHEREUM: "https://cloudflare-eth.com"
	}

	domain = Domain(
	    name="ThetanutsVault",
	    version="1",
	    chainId=current_chain.value,
	    verifying_contract=thetanutsSmartParadigm
	)

Interface to Thetanuts 

	thetanuts = Thetanuts(domain, rpc)

	

## Sign Bid

To sign a bid, given an auction ID from Paradigm

	from thetanuts.definitions import Bid
	from thetanuts.wallet import Wallet

	Define the following variables:
	wallet_public_key = "..."
	wallet_private_key = "..."

	payload = Bid(
	    rfqId=1,
	    signerWallet=wallet_public_key,
	    buyAmount=100000000,            # Bidder buys buyAmount
	    sellAmount=100000               # with sellAmount
	)

	wallet = Wallet(public_key=wallet_public_key, private_key=wallet_private_key)
	bid = wallet.sign_bid(domain, payload)

	# buyAmounts and sellAmounts are in terms of the underlying, 
	# so will need to consider the decimals (e.g. 6 decimals for USDC, 8 for WBTC, 18 for WETH)
	# buyAmounts must be equal to get_active_auctions().amountOffered 
	
## Validate Bids

	result = thetanuts.validate_bid(bid)
	print(result)
	# If the Bid is valid, we see
	# {'errors': 0}

	result = thetanuts.validate_bid(invalid_bid)
	print(result)
	# Examples of errors we get
	# {'errors': 5,
	#  'messages': ['BID_TOO_SMALL',         # Thetanuts vaults are winner-takes-all
	#               'PRICE_TOO_LOW',
	#               'SIGNER_ALLOWANCE_LOW',
	#               'SIGNER_BALANCE_LOW']}

## Set Allowance for Wallet

	thetanuts.approve_allowance(wallet, rfcId, amountToApprove = 2**256-1) 

	# Onchain transation will be created and broadcasted.
	# Default is unlimited approval; taker can also set it to precisely their sellAmount

## Validate Wallet

	check = thetanuts.verify_allowance(bidder_address, rfcId)
	print(check)

	# Returns {"allowanceSet": True} if allowance > 0
	# Bids may still fail validation if MMs dont do infinite approval; 
	#  e.g. they approved only 1000 USDC

## Get Information about Vault from On-chain calls
		
	vault = thetanuts.get_vault_details(verifying_contract)

	# Example of return
	# {"rfqId": 0, "chainId": 1, "collateralAsset": <ADDRESS_OF_USDC>, "expiryTimestamp": 16...., "optionType": "CALL", "strikeAsset": <ADDRESS_OF_USDC>, "strikePrice": "1250.5", "underlyingAsset": <ADDRESS_OF_WETH>, "numberOfContracts": 1000 }
	
## Thetanuts Backend

 1. Thetanuts service will poll for all the bids from Paradigm.
 2. Bid is accepted when a signed bid (paradigmID, vaultAddress, offerSize, expiryTime, bidderAddress, signature) from Paradigm is submitted to the smart contract


## Market Maker flow

0. Set Allowance For Wallet - We need a UI
1. Get offers and corresponding ID from Paradigm API
2. Sign Bid using Thetanuts SDK
4. Submit Bid via Paradigm API


## Thetanuts Flow
1. Create offer using Paradigm API, getting rfcID 

		POST /v1/vrfq/rfqs/
	```json
		{	
		  "domain": {
		    "contract_name": "string",
		    "version": "string",
		    "chain_id": 0,
		    "verifying_contract": "0xethput" 
		  },
		  "quantity": "string",
		  "swap_id": 0,  # Unique identifier for each verifying_contract - epoch for Thetanuts
		  "venue": "BLT" # NUT
		}
	```	
		DELETE  /v1/vrfq/rfqs/{id}
		# Cancel auction

2. Poll all signed bids with rfcID using Paradigm API

		GET /v1/vrfq/rfqs/{id}/quotes
	```json
	  "id": 0,
	  "bids": [
	    {
	      "id": 0,
	      "created": 0,
	      "maker": "string",
	      "price": "-49501926395530088",
	      "quantity": ".624",
	      "rfq_id": 0,
	      "status": "FillOrderStatus.OPEN"
	    }
	  ]
	```
4. Choose winning bid trade_id, get signature from Paradigm

		GET /v1/vrfq/quotes/{trade_id}

5. Submit to Thetanuts contract

5. Update Paradigm that the order has been taken

		PUT /v1/vrfq/trades/{trade_id}/
