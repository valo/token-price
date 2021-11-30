import threading
import time
import os
import traceback
import math
from brownie import interface
from brownie.network.account import Account
from prometheus_client import Gauge
from requests.exceptions import HTTPError
from . import master_chef
from . import staking_rewards
from .utils import priceOf, priceOfUniPair, priceOfCurveLPToken, priceOfCurvePool

NETWORK = os.environ.get("NETWORK", "ethereum")

FARM_TVL = Gauge("farm_tvl_dollars", "Farm TVL in dollars", ["network", "project", "staked_token"])
FARM_APR = Gauge("farm_apr_percent", "Farm APR in percent as 0-1.0", ["network", "project", "staked_token"])
PRICE = Gauge("price", "Price of the token on a DEX", ["network", "ticker", "dex", "version"])
BALANCE = Gauge("balance", "Balance of an address of native tokens", ["network", "address"])
K_GROWTH_SQRT = Gauge("k_growth_sqrt", "Tracks the sqrt(k)/lp_tokens of the pool, which allows to track the amount of fees accumulated over time", ["network", "ticker", "dex"])

VAULT_TVL_DOLLARS = Gauge("tvl_dollars", "TVL in dollars", ["network", "project", "ticker", "version"])
VAULT_TOTAL_ASSETS = Gauge("vault_total_assets", "Total amount of assets in the vault in the native token", ["network", "project", "ticker",  "version"])
VAULT_LOCKED_PROFIT = Gauge("vault_locked_profit", "The amount of locked profit in the vault", ["network", "project", "ticker",  "version"])
VAULT_UTILIZATION = Gauge("utilization_percent", "The percent of the utilized assets by a vault", ["network", "ticker",  "version"])
VAULT_LAST_REPORT = Gauge("last_report", "The timestamp of the last report of a vault", ["network", "ticker", "version"])


def update_metrics():
  if NETWORK == "bsc":
    from .networks.bsc import MASTER_CHEF_FARMS, TOKEN_PRICES, STAKING_REWARDS_FARMS, ADDRESS_BALANCES
    BLOCK_TIME = 3
  elif NETWORK == "matic":
    from .networks.matic import MASTER_CHEF_FARMS, TOKEN_PRICES, STAKING_REWARDS_FARMS, ADDRESS_BALANCES
    BLOCK_TIME = 2
  elif NETWORK == "ethereum":
    from .networks.ethereum import MASTER_CHEF_FARMS, TOKEN_PRICES, STAKING_REWARDS_FARMS, ADDRESS_BALANCES
    BLOCK_TIME = 15
  elif NETWORK == "heco":
    from .networks.heco import MASTER_CHEF_FARMS, TOKEN_PRICES, STAKING_REWARDS_FARMS, ADDRESS_BALANCES
    BLOCK_TIME = 3
  elif NETWORK == "arbitrum":
    from .networks.arbitrum import MASTER_CHEF_FARMS, TOKEN_PRICES, STAKING_REWARDS_FARMS, ADDRESS_BALANCES
    BLOCK_TIME = 1
  elif NETWORK == "avalanche":
    from .networks.avalanche import MASTER_CHEF_FARMS, TOKEN_PRICES, STAKING_REWARDS_FARMS, ADDRESS_BALANCES
    BLOCK_TIME = 1
  elif NETWORK == "fantom":
    from .networks.fantom import MASTER_CHEF_FARMS, TOKEN_PRICES, STAKING_REWARDS_FARMS, ADDRESS_BALANCES
    BLOCK_TIME = 1

  def update_prices():
    for dex in TOKEN_PRICES():
      router, tokens = TOKEN_PRICES()[dex]

      for ticker, address in tokens:
        try:
          version = "1.0"
          if address._name == "UniswapPair":
            price = priceOfUniPair(address, router_address=router)

            reserve1, reserve2, _timestamp = address.getReserves()
            lp_tokens = address.totalSupply()
            K_GROWTH_SQRT.labels(NETWORK, ticker, dex).set(math.sqrt(reserve1 * reserve2)/lp_tokens)
          elif address._name == "CurveLPToken":
            price = priceOfCurveLPToken(address, router_address=router)
          elif address._name == "CurvePool":
            price = priceOfCurvePool(address, router_address=router)
          elif address._name == "yEarnVault":
            price = address.pricePerShare() / 10 ** address.decimals()

            underlying_token = interface.IERC20(address.token())
            underlying_price = priceOf(underlying_token, router_address=router)
            decimals = underlying_token.decimals()
            total_assets = address.totalAssets() / 10**decimals
            total_debt = address.totalDebt() / 10**decimals
            version = address.apiVersion()
            VAULT_TVL_DOLLARS.labels(NETWORK, ticker, ticker, version).set(total_assets * underlying_price)
            if total_assets > 0:
              VAULT_UTILIZATION.labels(NETWORK, ticker, version).set(total_debt / total_assets)
            else:
              VAULT_UTILIZATION.labels(NETWORK, ticker, version).set(0)

            VAULT_LAST_REPORT.labels(NETWORK, ticker, version).set(address.lastReport())
            VAULT_TOTAL_ASSETS.labels(NETWORK, ticker, ticker, version).set(address.totalAssets())
            VAULT_LOCKED_PROFIT.labels(NETWORK, ticker, ticker, version).set(address.lockedProfit())
          else:
            price = priceOf(address, router_address=router)

          PRICE.labels(NETWORK, ticker, dex, version).set(price)
        except ValueError as e:
          print(f"Error while fetching price of {ticker}")
          traceback.print_exc()

  def update_master_chef_farms():
    for farm in MASTER_CHEF_FARMS():
      contract, reward_address_method_name, reward_per_block_method_name, router_address, stake_tokens = MASTER_CHEF_FARMS()[farm]

      for stake_token_name, stake_token in stake_tokens:
        try:
          tvl, apy = master_chef.fetch_farm_info(
            contract,
            stake_token,
            reward_address_method_name,
            reward_per_block_method_name,
            BLOCK_TIME,
            router_address
          )

          FARM_TVL.labels(NETWORK, farm, stake_token_name).set(tvl)
          FARM_APR.labels(NETWORK, farm, stake_token_name).set(apy)
        except ValueError as e:
          print(f"Error while fetching APY for {farm} {stake_token_name}")
          traceback.print_exc()

  def update_staking_rewards_farms():
    for farm in STAKING_REWARDS_FARMS():
      router_address, stake_tokens = STAKING_REWARDS_FARMS()[farm]

      for stake_token_name, stake_contract in stake_tokens:
        try:
          tvl, apy = staking_rewards.fetch_farm_info(
            stake_contract,
            router_address
          )

          FARM_TVL.labels(NETWORK, farm, stake_token_name).set(tvl)
          FARM_APR.labels(NETWORK, farm, stake_token_name).set(apy)
        except ValueError as e:
          print(f"Error while fetching APY for {farm} {stake_token_name}")
          traceback.print_exc()

  def update_address_balances():
    for address in ADDRESS_BALANCES:
      try:
        balance = Account(address).balance().to("ether")

        BALANCE.labels(NETWORK, address).set(balance)
      except ValueError as e:
        print(f"Error while balance of {address}: {e}")
        traceback.print_exc()

  while True:
    try:
      update_prices()

      update_master_chef_farms()

      update_staking_rewards_farms()

      update_address_balances()
    except HTTPError as e:
      if e.response.status_code == 429:
        print(f"Rate limited: {e}")
      else:
        print(f"HTTP Error: {e}")
    except Exception as e:
      print(f"Exception while updating metrics: {e}")
      traceback.print_exc()

    time.sleep(int(os.environ.get('METRICS_SLEEP_SEC', 15)))

def run():
  threading.Thread(target=update_metrics, name="Metrics", daemon=True).start()
