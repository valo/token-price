# Token price API

Return the price of tokens and uniswap pairs for a given address

## Setup

Install the required packages:

```
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and put your Infura Project ID in it.

## Usage

Run the server with:

```
flask run
```

To get the current UNI price open https://127.0.0.1:5000/token_price/0x1f9840a85d5af5bf1d1762f925bdaddc4201f984

To get the current ETH/UNI Uniswap LP token price open https://127.0.0.1:5000/uniswap_pair_price/0xd3d2e2692501a5c9ca623199d38826e513033a17
