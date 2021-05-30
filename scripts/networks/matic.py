from brownie import interface
from functools import lru_cache

QUICKSWAP_ROUTER = "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff"
DFYN_ROUTER = "0xA102072A4C07F06EC3B4900FDC4C7B80b6c57429"
SUSHI_ROUTER = "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506"

SUSHI_ETH_USDC = interface.UniswapPair("0x34965ba0ac2451a34a0471f04cca3f990b8dea27")
SUSHI_ETH_DAI = interface.UniswapPair("0x6ff62bfb8c12109e8000935a6de54dad83a4f39f")
SUSHI_ETH_USDT = interface.UniswapPair("0xc2755915a85c6f6c1c0f3a86ac8c058f11caa9c9")
SUSHI_FRAX_USDC = interface.UniswapPair("0x9e20a8d3501bf96eda8e69b96dd84840058a1cb0")

@lru_cache()
def TOKEN_PRICES():
  MATIC_ETH = interface.IERC20("0x7ceb23fd6bc0add59e62ac25578270cff1b9f619")
  MATIC_BTC = interface.IERC20("0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6")
  MATIC_QUICK = interface.IERC20("0x831753dd7087cac61ab5644b308642cc1c33dc13")
  MATIC_MATIC = interface.IERC20("0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270")
  MATIC_DFYN = interface.IERC20("0xc168e40227e4ebd8c1cae80f7a55a4f0e6d66c97")

  QUICK_ETH_USDC = interface.UniswapPair("0x853ee4b2a13f8a742d64c8f088be7ba2131f670d")
  QUICK_ETH_DAI = interface.UniswapPair("0x4a35582a710e1f4b2030a3f826da20bfb6703c09")
  QUICK_ETH_USDT = interface.UniswapPair("0xF6422B997c7F54D1c6a6e103bcb1499EeA0a7046")

  DFYN_ETH_USDC = interface.UniswapPair("0x7d51bad48d253dae37cc82cad07f73849286deec")
  DFYN_ETH_USDT = interface.UniswapPair("0x5d577d6cdc82d7b6cac7a101766b68f45bc3e34e")

  return {
  "Sushi-Polygon": (
    SUSHI_ROUTER,
    [
      ("ETH_USDC", SUSHI_ETH_USDC),
      ("ETH_DAI", SUSHI_ETH_DAI),
      ("ETH_USDT", SUSHI_ETH_USDT),
      ("FRAX_USDC", SUSHI_FRAX_USDC),
    ]
  ),
  "Quickswap": (
    QUICKSWAP_ROUTER,
    [
      ("ETH", MATIC_ETH),
      ("BTC", MATIC_BTC),
      ("QUICK", MATIC_QUICK),
      ("MATIC", MATIC_MATIC),
      ("ETH_USDC", QUICK_ETH_USDC),
      ("ETH_DAI", QUICK_ETH_DAI),
      ("ETH_USDT", QUICK_ETH_USDT),
    ]
  ),
  "DFYN": (
    DFYN_ROUTER,
    [
      ("DFYN", MATIC_DFYN),
      ("ETH_USDC", DFYN_ETH_USDC),
      ("ETH_USDT", DFYN_ETH_USDT),
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
  USDT_ETH_STAKING = interface.StakingRewards("0xB26bfcD52D997211C13aE4C35E82ced65AF32A02")

  return {
  "QuickSwap": (
    QUICKSWAP_ROUTER,
    [
      ("ETH_USDC", ETH_USDC_STAKING),
      ("DAI_ETH", DAI_ETH_STAKING),
      ("USDT_ETH", USDT_ETH_STAKING),
    ]
  ),
}
