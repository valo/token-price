from functools import lru_cache
from brownie import interface

PANCAKEV2_ETH_USDC = interface.UniswapPair("0xEa26B78255Df2bBC31C1eBf60010D78670185bD0")
PANCAKEV2_ETH_BTCB = interface.UniswapPair("0xD171B26E4484402de70e3Ea256bE5A2630d7e88D")
PANCAKEV2_BTCB_BUSD = interface.UniswapPair("0xf45cd219aef8618a92baa7ad848364a158a24f33")
PANCAKEV2_BTCB_BUSD = interface.UniswapPair("0xf45cd219aef8618a92baa7ad848364a158a24f33")

PANCAKESWAPV2_ROUTER = "0x10ED43C718714eb63d5aA57B78B54704E256024E"

BSC_DAI = interface.IERC20("0x1af3f329e8be154074d8769d1ffa4ee058b1dbc3")
BSC_BUSD = interface.IERC20("0xe9e7cea3dedca5984780bafc599bd69add087d56")
BSC_USDT = interface.IERC20("0x55d398326f99059ff775485246999027b3197955")
BSC_USDC = interface.IERC20("0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d")
BSC_VAI = interface.IERC20("0x4bd17003473389a42daf6a0a729f6fdb328bbbd7")
BSC_ETH = interface.IERC20("0x2170ed0880ac9a755fd29b2688956bd959f933f8")
BSC_BTC = interface.IERC20("0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c")
BSC_BNB = interface.IERC20("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")

@lru_cache
def TOKEN_PRICES():
  return {
  "PancakeSwapV2": (
    PANCAKESWAPV2_ROUTER,
    [
      ("ETH", BSC_ETH),
      ("BTC", BSC_BTC),
      ("BNB", BSC_BNB),
      ("ETH_USDC", PANCAKEV2_ETH_USDC),
      ("ETH_BTCB", PANCAKEV2_ETH_BTCB),
      ("BTCB_BUSD", PANCAKEV2_BTCB_BUSD),
    ]
  ),
}

@lru_cache
def MASTER_CHEF_FARMS():
  PANCAKEV2_MASTER_CHEF = interface.PancakeMasterChef("0x73feaa1eE314F8c655E354234017bE2193C9E24E")

  return {
  "PancakeSwapV2": (
    PANCAKEV2_MASTER_CHEF,
    "cake",
    "cakePerBlock",
    PANCAKESWAPV2_ROUTER,
    [
      ("ETH_USDC", PANCAKEV2_ETH_USDC),
    ]
  ),
}

@lru_cache()
def MASTER_CHEF_FARMS_V2():
  return {}

@lru_cache
def STAKING_REWARDS_FARMS():
  return {}
