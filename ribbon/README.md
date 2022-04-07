# Ribbon Finance SDK

Python SDK to interact with Ribbon Finance's systems.

Website: https://www.ribbon.finance

## Install

```bash
python3 -m pip install "git+https://github.com/tradeparadigm/sdks.git#egg=ribbon&subdirectory=ribbon"
```

## Usage

Sign your bids:
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

Validate a signed bid:
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

Get a JWT signature:
```python

from ribbon.authenticate import Authenticator

apiKey = "..."      # your api key

auth = Authenticator(apiKey)
jwtSignature = auth.sign_jwt({"some": "payload"})
print(jwtSignature)
```
