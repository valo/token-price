from brownie import interface
from functools import lru_cache

SUSHISWAP_ROUTER = "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506"

ETH = interface.IERC20("0x82af49447d8a07e3bd95bd0d56f35241523fbab1")
BTC = interface.IERC20("0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f")
USDC = interface.IERC20("0xff970a61a04b1ca14834a43f5de4533ebddb5cc8")
USDT = interface.IERC20("0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9")
MIM = interface.IERC20("0xfea7a6a0b346362bf88a9e4a88416b77a57d6c2a")

@lru_cache()
def TOKEN_PRICES():
  SUSHI_USDC_ETH = interface.UniswapPair("0x905dfcd5649217c42684f23958568e533c711aa3")
  SUSHI_USDT_ETH = interface.UniswapPair("0xcb0e5bfa72bbb4d16ab5aa0c60601c438f04b4ad")
  SUSHI_MIM_ETH = interface.UniswapPair("0xb6dd51d5425861c808fd60827ab6cfbffe604959")

  return {
  "Sushi-Arbitrum": (
    SUSHISWAP_ROUTER,
    [
      ("ETH", ETH),
      ("BTC", BTC),
      ("MIM", MIM),
      ("USDC_ETH", SUSHI_USDC_ETH),
      ("USDT_ETH", SUSHI_USDT_ETH),
      ("MIM_ETH", SUSHI_MIM_ETH),
    ]
  ),
}

def MASTER_CHEF_FARMS():
  return {}

def STAKING_REWARDS_FARMS():
  return {}

ADDRESS_BALANCES = []
