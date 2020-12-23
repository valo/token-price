from brownie import interface
from brownie.exceptions import ContractNotFound
from datetime import datetime, timedelta
from functools import lru_cache

DAI = interface.ERC20("0x6b175474e89094c44da98b954eedeac495271d0f")
WETH = interface.ERC20("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
USDT = interface.ERC20("0xdac17f958d2ee523a2206206994597c13d831ec7")

@lru_cache
def getFactory(router):
  return interface.UniswapFactoryV2(router.factory())

@lru_cache
def getToken0(pair):
  return interface.ERC20(pair.token0())

@lru_cache
def getToken1(pair):
  return interface.ERC20(pair.token1())

@lru_cache
def getPair(factory, token0, token1):
  return interface.UniswapPair(factory.getPair(token0, token1))

def getReserves(token, otherToken, factory):
  try:
    pair = getPair(factory, token, otherToken)
  except ContractNotFound:
    return 0

  (token0Reserves, token1Reserves, _) = pair.getReserves()

  if token == getToken0(pair):
    return token0Reserves
  else:
    return token1Reserves

def getUSDCPath(token: interface.ERC20, router: interface.UniswapRouterV2):
  factory = getFactory(router)
  reservesInWETH = getReserves(token, WETH, factory)
  reservesInUSDC = getReserves(token, USDT, factory)
  reservesInDAI = getReserves(token, DAI, factory)

  maxReserves = max(reservesInDAI, reservesInUSDC, reservesInWETH)

  if reservesInDAI == maxReserves:
    return [token, DAI, USDT]

  if reservesInWETH == maxReserves:
    return [token, WETH, USDT]

  return [token, USDT]

def priceOf(token: interface.ERC20, router_address: str):
  router = interface.UniswapRouterV2(router_address)
  return router.getAmountsOut(10 ** token.decimals(), getUSDCPath(token, router))[-1] / 10 ** USDT.decimals()

def priceOfUniPair(uni_pair: interface.UniswapPair, router_address: str):
  (token0Reserves, token1Reserves, _) = uni_pair.getReserves()

  token0 = getToken0(uni_pair)
  token1 = getToken1(uni_pair)

  token0Price = priceOf(token0, router_address)
  token1Price = priceOf(token1, router_address)

  total_pool = token0Reserves * token0Price / 10 ** token0.decimals() + token1Reserves * token1Price / 10 ** token1.decimals()

  return total_pool / uni_pair.totalSupply() * 10 ** uni_pair.decimals()
