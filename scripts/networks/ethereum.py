from brownie import interface

UNISWAP_ROUTER = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"

ETH = interface.IERC20("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
BTC = interface.IERC20("0x2260fac5e5542a773aa44fbcfedf7c193bc2c599")
UNI = interface.IERC20("0x1f9840a85d5af5bf1d1762f925bdaddc4201f984")
SUSHI = interface.IERC20("0x6b3595068778dd592e39a122f4f5a5cf09c90fe2")
ONE_INCH = interface.IERC20("0x111111111117dc0aa78b770fa6a738034120c302")

TOKEN_PRICES = {
  "Uniswap": (
    UNISWAP_ROUTER,
    [
      ("ETH", ETH),
      ("BTC", BTC),
      ("UNI", UNI),
      ("SUSHI", SUSHI),
      ("1INCH", ONE_INCH),
    ]
  )
}

MASTER_CHEF_FARMS = {
}

STAKING_REWARDS_FARMS = {
}
