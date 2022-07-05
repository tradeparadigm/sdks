# OPYN SDK

## Install

It's possible to install the package via `pip`,
having also `git` installed.

```bash
# Latest version
python3 -m pip install \
    "git+https://github.com/tradeparadigm/sdks.git#egg=opyn&subdirectory=opyn"
```

## Usage

There are different things you are able to do with this package.

### Define domain 

```python
from opyn.definitions import Chains, ContractConfig, Domain
from opyn.settlement import SettlementContract, asdict

# Define the following variables:
rpc_token = "..."
settlements_address = "0x..."
current_chain = Chains.ROPSTEN

rpc = {Chains.ROPSTEN: "https://ropsten.infura.io/v3/"}
chain_data = {
    "chain_id": current_chain,
    "rpc_uri": rpc[current_chain] + rpc_token,
}

settlement_config = ContractConfig(address=settlements_address, **chain_data)
settlement_contract = SettlementContract(settlement_config)

domain = Domain(
    name="OPYN RFQ",
    version="1",
    chainId=current_chain.value,
    verifyingContract=settlement_config.address,
)
print(asdict(domain))
```

This may output something similar to:
```python
{'name': 'OPYN RFQ', 'version': '1', 'chainId': 3, 'verifyingContract': '0x...'}
```

### Create offer

```python
import os
from opyn.definitions import *
from opyn.settlement import SettlementContract
from dotenv import load_dotenv

load_dotenv()

rpc_token = os.getenv('RPC_TOKEN')
current_chain = Chains.ROPSTEN
rpc = {
    Chains.ROPSTEN: os.getenv('RPC_URL')
}
rpc_uri = rpc[current_chain] + rpc_token

settlement_contract_address = "0x73834097f5e7c8a8b2465c80a8362d8737d8c8cd"
settlement_config = ContractConfig(settlement_contract_address, rpc_uri, current_chain)
settlement_contract = SettlementContract(settlement_config)

taker_public = "0x..."
taker_private = "0x..."
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
```

### Signing bid order

```python
from opyn.definitions import MessageToSign
from opyn.wallet import Wallet

wallet_public_key = ""
wallet_private_key = ""
usdc_token_address = "0x..."
osqth_token_address = "0x.."

payload = MessageToSign(
    offerId="1",
    bidId="1",
    signerAddress=wallet_public_key,
    bidderAddress=wallet_public_key,
    bidToken=usdc_token_address,
    offerToken=osqth_token_address,
    bidAmount=1e18,
    sellAmount=1000e6,
    nonce="1"
)

wallet = Wallet(public_key=wallet_public_key, private_key=wallet_private_key)

signed_bid = wallet.sign_bid_data(domain, payload)
pprint(asdict(signed_bid))
```

### Validate signed bid

```python
result = settlement_contract.validate_bid(signed_maker_order)
print(result)
```

Example output
```
{
    'errors': 4, 
    'messages': [
        'SIGNATURE_MISMATCHED', 
        'BID_EXCEED_TOTAL_SIZE', 
        'BIDDER_ALLOWANCE_LOW', 
        'SELLER_ALLOWANCE_LOW'
    ]                       
}
```                                                         

### Fetching offer details

```python
import os
from opyn.definitions import *
from opyn.settlement import SettlementContract
from dotenv import load_dotenv

load_dotenv()

rpc_token = os.getenv('RPC_TOKEN')
current_chain = Chains.ROPSTEN
rpc = {
    Chains.ROPSTEN: os.getenv('RPC_URL')
}
rpc_uri = rpc[current_chain] + rpc_token

settlement_contract_address = "0x73834097f5e7c8a8b2465c80a8362d8737d8c8cd"
settlement_config = ContractConfig(settlement_contract_address, rpc_uri, current_chain)
settlement_contract = SettlementContract(settlement_config)

offer_details = settlement_contract.get_offer_details(offerId)
```

### Validate wallets

```python

# Define the following variables:
token_address = "0x..."

check = wallet.verify_allowance(settlement_config=settlement_config, token_address=token_address)
print(check)

# True
```

## Local development

- Install dependencies using poetry by running `poetry install`
- Build module by running `poetry build`

### How to run test file

- Make sure to have the following environment variables in `.env` file:
```
RPC_TOKEN=
RPC_URL=
MAKER_PubKEY=
MAKER_PrivKEY=
TAKER_PubKEY=
TAKER_PrivKEY=
```
- Make sure to build the Opyn module
- Run `pip3 install -I opyn/dist/opyn-0.1.0-py3-none-any.whl`
- Run python3 opyn_test.py

## Settlement Contract Addresses

- Mainnet:
- Ropsten: 0x635f8703b4E00357C5a323424423e001c07b8f65