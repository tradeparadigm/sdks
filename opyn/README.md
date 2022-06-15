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

### Signing bid order

```python
from opyn.definitions import MessageToSign
from opyn.wallet import Wallet

wallet_public_key = ""
wallet_private_key = ""

payload = MessageToSign(
    bidId="1",
    trader=wallet_public_key
    nonce="1",
    token="0xabcd",
    amount="6000000",
    buyAmount=1000000000000000000,
    referrer="0x0000000000000000000000000000000000000000",
)

wallet = Wallet(public_key=wallet_public_key, private_key=wallet_private_key)

bid = wallet.sign_bid(domain, payload)
pprint(asdict(bid))
```

### Fetching offer details

### Executing settlement

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
RELAYER_API=
```
- Make sure to build the Opyn module
- Run `pip3 install -I opyn/dist/opyn-0.1.0-py3-none-any.whl`
- Run python3 opyn_test.py