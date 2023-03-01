import os
import traceback
from brownie import interface
from brownie.exceptions import ContractNotFound
from functools import lru_cache
from typing import List, Callable

@lru_cache
def DAI() -> interface.IERC20:
  return interface.IERC20(os.environ.get('DAI_ADDRESS', "0x6b175474e89094c44da98b954eedeac495271d0f"))

@lru_cache
def WETH() -> interface.IERC20:
  return interface.IERC20(os.environ.get('WETH_ADDRESS', "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"))

@lru_cache
def USDT() -> interface.IERC20:
  return interface.IERC20(os.environ.get('USDT_ADDRESS', "0xdac17f958d2ee523a2206206994597c13d831ec7"))

@lru_cache
def USDC() -> interface.IERC20:
  return interface.IERC20(os.environ.get('USDC_ADDRESS', "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"))

@lru_cache
def getFactory(router) -> interface.UniswapFactoryV2:
  return interface.UniswapFactoryV2(router.factory())

@lru_cache
def getToken0(pair) -> interface.IERC20:
  return interface.IERC20(pair.token0())

@lru_cache
def getToken1(pair) -> interface.IERC20:
  return interface.IERC20(pair.token1())

@lru_cache
def getPair(factory, token0, token1) -> interface.UniswapPair:
  return interface.UniswapPair(factory.getPair(token0, token1))

def getReserves(token, otherToken, factory) -> float:
  try:
    pair = getPair(factory, token, otherToken)
  except ContractNotFound:
    return 0

  (token0Reserves, token1Reserves, _) = pair.getReserves()

  if token == getToken0(pair):
    return token0Reserves / 10**(token.decimals())
  else:
    return token1Reserves / 10**(token.decimals())

def getUSDCPath(token: interface.IERC20, router: interface.UniswapRouterV2) -> List[interface.IERC20]:
  factory = getFactory(router)
  if token != WETH():
    reservesInWETH = getReserves(WETH(), token, factory) * priceOf(WETH(), router)
  else:
    reservesInWETH = 0

  reservesInUSDT = getReserves(USDT(), token, factory)
  reservesInUSDC = getReserves(USDC(), token, factory)
  reservesInDAI = getReserves(DAI(), token, factory)

  maxReserves = max(reservesInDAI, reservesInUSDC, reservesInWETH, reservesInUSDT)

  if reservesInDAI == maxReserves:
    return [token, DAI()]

  if reservesInWETH == maxReserves:
    return [token, WETH(), USDC()]

  if reservesInUSDT == maxReserves:
    return [token, USDT()]

  return [token, USDC()]

def priceOf(token: interface.IERC20, router_address: str) -> float:
  if token == USDC() or token == USDT():
    return 1.0

  router = interface.UniswapRouterV2(router_address)
  path = getUSDCPath(token, router)
  return router.getAmountsOut(10 ** token.decimals() / 100, path)[-1] / 10 ** path[-1].decimals() * 100

def priceOfyEarnVaultShare(token: interface.IERC20, router_address: str) -> float:
  yearn_vault = interface.yEarnVault(token)
  underlying_price = price_unknown_token(yearn_vault.token(), router=router_address)

  vault_total_supply = yearn_vault.totalSupply()
  vault_balance = yearn_vault.totalAssets()

  return underlying_price * vault_balance / vault_total_supply

def priceOfUniPair(uni_pair: interface.UniswapPair, router_address: str) -> float:
  (token0Reserves, token1Reserves, _) = uni_pair.getReserves()

  token0 = getToken0(uni_pair)
  token0Price = priceOf(token0, router_address)

  token1 = getToken1(uni_pair)
  token1Price = priceOf(token1, router_address)

  total_pool = token0Reserves * token0Price / 10 ** token0.decimals() + token1Reserves * token1Price / 10 ** token1.decimals()

  return total_pool / uni_pair.totalSupply() * 10 ** uni_pair.decimals()

def priceOf1InchPair(oneinch_pair: interface.IMooniswap, router_address: str) -> float:
  (token0, token1) = oneinch_pair.getTokens()

  if token0 == "0x0000000000000000000000000000000000000000":
    token0 = WETH()
    token0Reserves = oneinch_pair.balance()
  else:
    token0 = interface.IERC20(token0)
    token0Reserves = token0.balanceOf(oneinch_pair)

  if token1 == "0x0000000000000000000000000000000000000000":
    token1 = WETH()
    token1Reserves = oneinch_pair.balance()
  else:
    token1 = interface.IERC20(token1)
    token1Reserves = token1.balanceOf(oneinch_pair)


  token0Price = priceOf(token0, router_address)
  token1Price = priceOf(token1, router_address)

  total_pool = token0Reserves * token0Price / 10 ** token0.decimals() + token1Reserves * token1Price / 10 ** token1.decimals()

  return total_pool / oneinch_pair.totalSupply() * 10 ** oneinch_pair.decimals()

def price_curve_pool(lp_token: interface.CurvePool, balances: List[int], get_coin: Callable[[int], interface.ERC20], get_dy, router_address:str):
  if len(balances) == 0:
    raise ValueError(f"Can't get balances for curve lp token {lp_token}")

  priced_token_index = None
  token_prices = []
  decimals = []
  coins = []

  for index, balance in enumerate(balances):
    coin_address = get_coin(index)
    if coin_address == "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE":
      coin = WETH()
    else:
      coin = interface.ERC20(coin_address)

    coins.append(coin)
    decimals.append(coin.decimals())
    price = price_unknown_token(coin, router_address)
    token_prices.append(price)

    if price and priced_token_index is None:
      priced_token_index = index

  if None in token_prices and priced_token_index is not None:
    # Price the remaining tokens using the priced token
    for index, balance in enumerate(balances):
      if token_prices[index]:
        continue

      dy = get_dy(index, priced_token_index, 10 ** decimals[index])
      token_prices[index] = dy * token_prices[priced_token_index] / 10 ** decimals[priced_token_index]

  if None in token_prices:
    raise ValueError(f"Can't price {lp_token}")

  total_dollars_locked = 0
  for coin, price, balance, decimals in zip(coins, token_prices, balances, decimals):
    total_dollars_locked += price * balance / 10 ** decimals

  total_supply = lp_token.totalSupply() / 10 ** lp_token.decimals()
  return total_dollars_locked / total_supply

def priceOfCurveLPToken(lp_token: interface.CurveLPToken, router_address: str) -> float:
  minter = interface.CurveLPMinter(lp_token.minter())

  balances = []
  for index in range(5):
    try:
      balances.append(minter.balances(index))
    except ValueError:
      break

  return price_curve_pool(lp_token, balances, minter.coins, minter.get_dy, router_address)

def priceOfCurvePool(lp_token: interface.CurvePool, router_address: str) -> float:
  return price_curve_pool(lp_token, lp_token.get_balances(), lp_token.coins, lp_token.get_dy, router_address)

def homoraV2PositionSize(pos_id: int, bank_address: str, router_address: str) -> float:
  bank = interface.HomoraBank(bank_address)

  (_owner, coll_token, coll_id, coll_size) = bank.getPositionInfo(pos_id)
  coll = interface.WMasterChef(coll_token)

  underlying_lp_token = interface.UniswapPair(coll.getUnderlyingToken(coll_id))
  position_size = priceOfUniPair(underlying_lp_token, router_address) * coll_size / 10 ** underlying_lp_token.decimals()

  debts = bank.getPositionDebts(pos_id)
  total_debt = 0

  for (debt_token, debt_size) in zip(*debts):
    debt_token = interface.ERC20(debt_token)
    total_debt += priceOf(debt_token, router_address) * debt_size / 10 ** debt_token.decimals()

  return position_size - total_debt

# Sometimes we need to detect what type of token we are dealing with, so we try a couple of
# contracts to extract the price
def price_unknown_token(token, router: str):
  # Try an Aave V2 aToken
  try:
    atoken = interface.AToken(token)
    underlying = interface.IERC20(atoken.UNDERLYING_ASSET_ADDRESS())
    price_of_underlying = priceOf(underlying, router_address=router)
    return price_of_underlying
  except ValueError as e:
    # print(f"Error while fetching price of {token}: {e}")
    # traceback.print_exc()
    pass

  # Try Curve LP Token with a minter
  try:
    curve_lp = interface.CurveLPToken(token)
    return priceOfCurveLPToken(curve_lp, router_address=router)
  except ValueError as e:
    # print(f"Error while fetching price of {token}: {e}")
    # traceback.print_exc()
    pass

  # Try Curve LP Token without a minter
  try:
    curve_lp = interface.CurvePool(token)
    return priceOfCurvePool(curve_lp, router_address=router)
  except ValueError as e:
    # print(f"Error while fetching price of {token}: {e}")
    # traceback.print_exc()
    pass

  # Try a yEarn vault
  try:
    return priceOfyEarnVaultShare(token, router_address=router)
  except ValueError as e:
    # print(f"Error while fetching price of {token}: {e}")
    # traceback.print_exc()
    pass

  # Try to price as a regular ERC20 traded on a dex
  try:
    erc20 = interface.IERC20(token)
    return priceOf(erc20, router_address=router)
  except ValueError as e:
    # print(f"Error while fetching price of {token}: {e}")
    # traceback.print_exc()
    pass
  
  print(f"Can't price {token}")
  return None

def glpPrice(glp_manager):
  try:
    manager = interface.GlpManager(glp_manager)
    glp_token = interface.IERC20(manager.glp())

    aum = manager.getAum(0)
    total_supply = glp_token.totalSupply()

    return aum / total_supply / 10**12
  except ValueError:
    pass

  return 0

def glpTokenAum(vault, token):
  token_price = vault.getMaxPrice(token)
  poolAmount = vault.poolAmounts(token)
  decimals = vault.tokenDecimals(token)

  if (vault.stableTokens(token)):
    return poolAmount * token_price / 10 ** decimals
  else:
    aum = 0
    size = vault.globalShortSizes(token)
    if (size > 0):
      averagePrice = vault.globalShortAveragePrices(token)
      priceDelta = token_price - averagePrice

      delta = size * priceDelta / averagePrice

      aum += delta

    aum = aum + vault.guaranteedUsd(token)

    reservedAmount = vault.reservedAmounts(token)
    aum += (poolAmount - reservedAmount) * token_price / 10 ** decimals

    return aum

def glpWeight(glp_manager, token):
  manager = interface.GlpManager(glp_manager)
  vault = interface.GlpVault(manager.vault())
  
  glp_aum = manager.getAum(0)
  token_aum = glpTokenAum(vault, token)

  return token_aum / glp_aum

def glpRewards(rewards_tracker, address):
  tracker = interface.IRewardsTracker(rewards_tracker)

  claimable = tracker.claimable(address)
  decimals = tracker.decimals()

  return claimable / 10**decimals