# Ribbon Finance SDK

Python SDK to interact with Ribbon Finance's systems.

Website: https://www.ribbon.finance

## Install

It's possible to install the package via `pip`,
having also `git` installed.

```bash
# Latest version
python3 -m pip install \
    "git+https://github.com/tradeparadigm/sdks.git#egg=ribbon&subdirectory=ribbon"

# A specific commit version
python3 -m pip install \
    "git+https://github.com/tradeparadigm/sdks.git@74554a57ef278791651ee3f5f7f7a1289ae20656#egg=ribbon&subdirectory=ribbon"
```

## Usage

There are different things you are able to do with this package.
First let's setup the needed informations.

This is an example of how we can define your domain of interaction:
```python
from ribbon.definitions import Chains, ContractConfig, Domain
from ribbon.swap import SwapContract, asdict

# Define the following variables:
rpc_token = "..."
swap_address = "0x..."
current_chain = Chains.KOVAN

rpc = {Chains.KOVAN: "https://kovan.infura.io/v3/"}
chain_data = {
    "chain_id": current_chain,
    "rpc_uri": rpc[current_chain] + rpc_token,
}

swap_config = ContractConfig(address=swap_address, **chain_data)
swap_contract = SwapContract(swap_config)

domain = Domain(
    name="RIBBON SWAP",
    version="1",
    chainId=current_chain.value,
    verifyingContract=swap_config.address,
)
print(asdict(domain))
```

This may output something similar to:
```python
{'chainId': 42,
 'name': 'RIBBON SWAP',
 'salt': None,
 'verifyingContract': '0x58848824baEb9678847aF487CB02EAba782FECB5',
 'version': '1'}
```

### Sign bids

```python
from ribbon.definitions import Bid
from ribbon.wallet import Wallet

# Define the following variables:
wallet_public_key = "..."
wallet_private_key = "..."

payload = Bid(
    swapId=1,
    nonce=1,
    signerWallet=wallet_public_key,
    sellAmount=6000000,
    buyAmount=1000000000000000000,
    referrer="0x0000000000000000000000000000000000000000",
)


wallet = Wallet(wallet_private_key)

bid = wallet.sign_bid(domain, payload)
pprint(asdict(bid))
```

This may output something similar to:
```python
{'buyAmount': 1000000000000000000,
 'nonce': 1,
 'r': '0xd48860fab24673d45a03d58428f36bd7d62ac115972bd2a94e040503415a9478',
 'referrer': '0x0000000000000000000000000000000000000000',
 's': '0x32eed933d6532dc613e3167a5e839bce2c1d577b3c4b2c73eea7411fec1c9a53',
 'sellAmount': 6000000,
 'signerWallet': '0x...',
 'swapId': 1,
 'v': 27}

```

### Validate bids

```python
result = swap_contract.validate_bid(bid)
print(result)
# If the Bid is valid, we see
# {'errors': 0}

result = swap_contract.validate_bid(invalid_bid)
print(result)
# Examples of errors we get
# {'errors': 5,
#  'messages': ['BID_TOO_SMALL',
#               'PRICE_TOO_LOW',
#               'SIGNER_ALLOWANCE_LOW',
#               'SIGNER_BALANCE_LOW']}
```

### Validate bids

```python

# Define the following variables:
token_address = "0x..."

check = wallet.verify_allowance(swap_config=swap_config, token_address=token_address)
print(check)

# True
```

### Informations about the Vaults

Get details related to the oToken of interest:
```python
from ribbon.otoken import oTokenContract

# Define the following variables:
otoken_address = "0x..."

oToken = oTokenContract(ContractConfig(address=otoken_address, **chain_data))
details = oToken.get_otoken_details()
print(details)
```

This may output something similar to:
```python
{'collateralAsset': '0xd0A1E359811322d97991E03f863a0C30C2cF029C',
 'expiryTimestamp': 1646380800,
 'isPut': False,
 'strikeAsset': '0x7e6edA50d1c833bE936492BF42C1BF376239E9e2',
 'strikePrice': 200000000000,
 'underlyingAsset': '0xd0A1E359811322d97991E03f863a0C30C2cF029C'}
```

### Produce a JWT signature

```python

from ribbon.authenticate import Authenticator

# Define the following variables:
api_key = "..."

auth = Authenticator(api_key)
jwtSignature = auth.sign_jwt({"some": "payload"})
print(jwtSignature)
```

## Development

To contribute to this package you may set up a dedicated container:
```bash
# open a container with python
$ docker run -it --rm \
    -v $(pwd):/tmp/code -w /tmp/code \
    -p 8888:8888 \
    python:3.10 \
    bash

# install the library in development mode
pip3 install -e ribbon/

# run code that accesses the ribbon sdk
python3 my_examples.py

# optional: add and use ipython/jypiter
pip3 install ipython jupyter
jupyter notebook --allow-root --no-browser --ip=0.0.0.0
# now browse the http://127.0.0.1:8888/?token=... link in the output
```
