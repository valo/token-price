from brownie import interface
from brownie.exceptions import ContractNotFound
from datetime import datetime, timedelta

DAI = interface.ERC20("0x6b175474e89094c44da98b954eedeac495271d0f")
WETH = interface.ERC20("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
USDC = interface.ERC20("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
UNISWAP_ROUTER = interface.UniswapRouterV2("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")
UNISWAP_FACTORY = interface.UniswapFactoryV2("0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f")

def getReserves(token, otherToken):
  try:
    pair = interface.UniswapPair(UNISWAP_FACTORY.getPair(token, otherToken))
  except ContractNotFound:
    return 0

  (token0Reserves, token1Reserves, _) = pair.getReserves()

  if token == pair.token0():
    return token0Reserves
  else:
    return token1Reserves

def getUSDCPath(token):
  reservesInWETH = getReserves(token, WETH)
  reservesInUSDC = getReserves(token, USDC)
  reservesInDAI = getReserves(token, DAI)

  maxReserves = max(reservesInDAI, reservesInUSDC, reservesInWETH)

  if reservesInDAI == maxReserves:
    return [token, DAI, USDC]

  if reservesInWETH == maxReserves:
    return [token, WETH, USDC]

  return [token, USDC]

def priceOf(token):
  return UNISWAP_ROUTER.getAmountsOut(10 ** token.decimals(), getUSDCPath(token))[-1] / 10 ** USDC.decimals()

def priceOfUniPair(uni_pair):
  (token0Reserves, token1Reserves, _) = uni_pair.getReserves()
  token0 = interface.ERC20(uni_pair.token0())
  token1 = interface.ERC20(uni_pair.token1())

  token0Price = priceOf(token0)
  token1Price = priceOf(token1)

  total_pool = token0Reserves * token0Price / 10 ** token0.decimals() + token1Reserves * token1Price / 10 ** token1.decimals()

  return total_pool / uni_pair.totalSupply() * 10 ** uni_pair.decimals()
