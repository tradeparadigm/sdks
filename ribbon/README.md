# Ribbon Finance SDK

Python SDK to interact with Ribbon Finance's systems.

Website: https://www.ribbon.finance

## Install

```bash
python3 -m pip install "git+https://github.com/tradeparadigm/sdks.git#egg=ribbon&subdirectory=ribbon"
```

## Usage

You can sign your bids:

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
