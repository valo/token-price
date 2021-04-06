from brownie import interface
from functools import lru_cache

MDEX_ROUTER = "0xED7d5F38C79115ca12fe6C0041abb22F0A06C300"

@lru_cache()
def TOKEN_PRICES():
  HUSD_USDT = interface.UniswapPair("0xdff86b408284dff30a7cad7688fedb465734501c")

  return {
  "MDex": (
    MDEX_ROUTER,
    [
      ("HUSD_USDT", HUSD_USDT),
    ]
  )
}

@lru_cache()
def MASTER_CHEF_FARMS():
  return {}

@lru_cache()
def STAKING_REWARDS_FARMS():
  return {}
