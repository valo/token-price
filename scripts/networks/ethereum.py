from brownie import interface
from functools import lru_cache

UNISWAP_ROUTER = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
SUSHISWAP_ROUTER = "0xd9e1ce17f2641f24ae83637ab66a2cca9c378b9f"

ETH = interface.IERC20("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
BTC = interface.IERC20("0x2260fac5e5542a773aa44fbcfedf7c193bc2c599")
UNI = interface.IERC20("0x1f9840a85d5af5bf1d1762f925bdaddc4201f984")
SUSHI = interface.IERC20("0x6b3595068778dd592e39a122f4f5a5cf09c90fe2")
YFI = interface.IERC20("0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e")
USDC = interface.IERC20("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
USDT = interface.IERC20("0xdac17f958d2ee523a2206206994597c13d831ec7")
AAVE = interface.IERC20("0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9")

@lru_cache()
def TOKEN_PRICES():
  ONE_INCH = interface.IERC20("0x111111111117dc0aa78b770fa6a738034120c302")
  DAI = interface.IERC20("0x6b175474e89094c44da98b954eedeac495271d0f")
  BUSD = interface.IERC20("0x4fabb145d64652a948d72533023f6e7a623c7c53")
  UWL = interface.IERC20("0xdbdd6f355a37b94e6c7d32fef548e98a280b8df5")
  COMP = interface.IERC20("0xc00e94cb662c3520282e6f5717214004a7f26888")
  LRC = interface.IERC20("0xbbbbca6a901c926f240b89eacb641d8aec7aeafd")

  SUSHI_ALPHA_ibETHv2 = interface.UniswapPair("0xf79a07cd3488bbafb86df1bad09a6168d935c017")
  SUSHI_ALCX_ETH = interface.UniswapPair("0xc3f279090a47e80990fe3a9c30d24cb117ef91a8")

  SUSHI_ALCX = interface.IERC20("0xdbdb4d16eda451d0503b854cf79d55697f90c8df")
  SUSHI_ANY = interface.IERC20("0xf99d58e463a2e07e5692127302c20a191861b4d6")

  return {
  "Uniswap": (
    UNISWAP_ROUTER,
    [
      ("ETH", ETH),
      ("BTC", BTC),
      ("UNI", UNI),
      ("SUSHI", SUSHI),
      ("1INCH", ONE_INCH),
      ("YFI", YFI),
      ("DAI", DAI),
      ("USDC", USDC),
      ("USDT", USDT),
      ("BUSD", BUSD),
      ("UWL", UWL),
      ("COMP", COMP),
      ("LRC", LRC),
      ("AAVE", AAVE),
    ]
  ),
  "SushiSwap": (
    SUSHISWAP_ROUTER,
    [
      ("ALPHA_ibETHv2", SUSHI_ALPHA_ibETHv2),
      ("ALCX", SUSHI_ALCX),
      ("ANY", SUSHI_ANY),
      ("ALCX_ETH", SUSHI_ALCX_ETH),
    ]
  ),
}

def MASTER_CHEF_FARMS():
  BDP_MASTER_CHEF = interface.BDPMaster("0x0De845955E2bF089012F682fE9bC81dD5f11B372")

  return {
    "BigDataProtocol": (
      BDP_MASTER_CHEF,
      "BDP",
      "REWARD_PER_BLOCK",
      UNISWAP_ROUTER,
      [
        ("USDT", USDT),
        ("USDC", USDC),
        ("ETH", ETH),
        ("BTC", BTC),
        ("YFI", YFI),
        ("UNI", UNI),
        ("AAVE", AAVE),
        ("SUSHI", SUSHI),
      ]
    ),
  }

def STAKING_REWARDS_FARMS():
  return {}
