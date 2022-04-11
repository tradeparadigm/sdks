# Ribbon Finance SDK

Python SDK to interact with Ribbon Finance's systems.

Website: https://www.ribbon.finance

## Install

```bash
python3 -m pip install "git+https://github.com/tradeparadigm/sdks.git#egg=ribbon&subdirectory=ribbon"
```

## Usage

There are different things you are able to do with this package.
First let's setup the needed informations.

This is an example of how we can define your domain of interaction:
```python
from ribbon.definitions import Chains, ContractConfig, Domain
from ribbon.swap import SwapContract, asdict


rpc_token = "0bccea5795074895bdb92c62c5c3afba"
swap_address = "0x58848824baEb9678847aF487CB02EAba782FECB5"

current_chain = Chains.KOVAN
rpc = {Chains.KOVAN: "https://kovan.infura.io/v3/"}
chain = {
    "chain_name": current_chain,
    "rpc_uri": rpc[current_chain] + rpc_token,
}

swap_config = ContractConfig(address=swap_address, **chain)
swap_contract = SwapContract(swap_config)

domain = Domain(
    name="RIBBON SWAP",
    version="1",
    chainId=current_chain,
    verifyingContract=swap_config.address,
)
asdict(domain)

```

### Sign bids

```python
from pprint import pprint
from dataclasses import asdict

from ribbon.classes import Domain, Bid
from ribbon.sign import Signature


domain = Domain(
    name="RIBBON SWAP",
    version="1",
    chainId=42,
    verifyingContract="0x...",
)

payload = Bid(
    swapId=1,
    nonce=1,
    signerWallet="0x...",
    sellAmount=6000000,
    buyAmount=1000000000000000000,
    referrer="0x0000000000000000000000000000000000000000",
)

priv_key = "..."            # your wallet private key

signer = Signature(priv_key)
bid = signer.sign_bid(domain, payload)
pprint(asdict(bid))

# {'buyAmount': 1000000000000000000,
#  'nonce': 1,
#  'r': '0x...',
#  'referrer': '0x0000000000000000000000000000000000000000',
#  's': '0x...',
#  'sellAmount': 6000000,
#  'signerWallet': '0x...',
#  'swapId': 1,
#  'v': 27}

```

### Validate bids

```python
from pprint import pprint

from ribbon.swap import SwapContract

rpc_url = "https://kovan.infura.io/v3/"
swap_address = "0x..."

rpc_token = "..."      # token for infura

swap = SwapContract(rpc_url, rpc_token, swap_address)

result = swap.validate_bid(this_is_a_valid_bid)
pprint(result)

# {'errors': 0}


result = swap.validate_bid(this_is_a_bad_bid)
pprint(result)

# {'errors': 5,
#  'messages': ['BID_TOO_SMALL',
#               'PRICE_TOO_LOW',
#               'SIGNER_ALLOWANCE_LOW',
#               'SIGNER_BALANCE_LOW']}

```

### Informations about the Vaults

Get details related to the oToken of interest:
```python
from pprint import pprint

from ribbon.option import oTokenContract


rpc_url = "https://kovan.infura.io/v3/"
otoken_address = "0x..."

rpc_token = "..."      # token for infura

oToken = oTokenContract(rpc_url, rpc_token, otoken_address)
details = oToken.get_otoken_details()
pprint(details)

# {'collateralAsset': '0x...',
#  'expiryTimestamp': 1646380800,
#  'isPut': False,
#  'strikeAsset': '0x...',
#  'strikePrice': 200000000000,
#  'underlyingAsset': '0x...'}

```

### Produce a JWT signature

```python

from ribbon.authenticate import Authenticator

apiKey = "..."      # your api key

auth = Authenticator(apiKey)
jwtSignature = auth.sign_jwt({"some": "payload"})
print(jwtSignature)
```

## Development

```bash
# open a container with the latest python
$ docker run -it --rm \
    -v $(pwd):/tmp/code -w /tmp/code \
    -p 8888:8888 \
    python:3.10 \
    bash

# install the library in development mode
pip3 install -e ribbon/

# run code that access the ribbon sdk
python3 my_examples.py

# optional: add and use ipython/jypiter
pip3 install ipython jupyter
jupyter notebook --allow-root --no-browser --ip=0.0.0.0
# now browse the http://127.0.0.1:8888/?token=... link in the output
```
