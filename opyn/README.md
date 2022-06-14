# OPYN SDK

## Local development

- Install dependencies using poetry by running `poetry install`
- Build module by running `poetry build`

## Signing bid order

## Fetching offer details

## Executing settlement

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