from brownie import interface
from functools import lru_cache

QUICKSWAP_ROUTER = "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff"

@lru_cache()
def TOKEN_PRICES():
  MATIC_ETH = interface.IERC20("0x7ceb23fd6bc0add59e62ac25578270cff1b9f619")
  MATIC_BTC = interface.IERC20("0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6")
  MATIC_QUICK = interface.IERC20("0x831753dd7087cac61ab5644b308642cc1c33dc13")
  MATIC_MATIC = interface.IERC20("0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270")

  QUICK_ETH_USDC = interface.UniswapPair("0x853ee4b2a13f8a742d64c8f088be7ba2131f670d")
  QUICK_ETH_DAI = interface.UniswapPair("0x4a35582a710e1f4b2030a3f826da20bfb6703c09")

  return {
  "Quickswap": (
    QUICKSWAP_ROUTER,
    [
      ("ETH", MATIC_ETH),
      ("BTC", MATIC_BTC),
      ("QUICK", MATIC_QUICK),
      ("MATIC", MATIC_MATIC),
      ("ETH_USDC", QUICK_ETH_USDC),
      ("ETH_DAI", QUICK_ETH_DAI),
    ]
  )
}

@lru_cache()
def MASTER_CHEF_FARMS():
  return {}

@lru_cache()
def STAKING_REWARDS_FARMS():
  ETH_USDC_STAKING = interface.StakingRewards("0x4A73218eF2e820987c59F838906A82455F42D98b")
  DAI_ETH_STAKING = interface.StakingRewards("0x785AaCd49c1Aa3ca573F2a32Bb90030A205b8147")

  return {
  "QuickSwap": (
    QUICKSWAP_ROUTER,
    [
      ("ETH_USDC", ETH_USDC_STAKING),
      ("DAI_ETH", DAI_ETH_STAKING),
    ]
  ),
}
