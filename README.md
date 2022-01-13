# Token price API

Return the price of tokens and uniswap pairs for a given address

## Setup

You can run the server using docker. First build the image:

```
docker build . -t token-price
```

Copy `.env.example` to `.env` and put an ETH RPC endpoint in it, which the server will use to connect.

Take a look at `brownie-config.yaml` for all the env variables for the different network RPCs.

## Usage

Run the server with:

```
docker run --env-file .env -p 5000:5000 token-price
```

To get the current UNI price open https://127.0.0.1:5000/token_price/0x1f9840a85d5af5bf1d1762f925bdaddc4201f984

To get the current ETH/UNI Uniswap LP token price open https://127.0.0.1:5000/uniswap_pair_price/0xd3d2e2692501a5c9ca623199d38826e513033a17

To open all the promethus metrics go to http://127.0.0.1:5000/metrics