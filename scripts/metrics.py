import threading
import time
import os
import traceback
from brownie import interface
from prometheus_client import Gauge
from . import master_chef
from . import staking_rewards
from .utils import priceOf

NETWORK = os.environ.get("NETWORK", "ethereum")

if NETWORK == "bsc":
  from .networks.bsc import MASTER_CHEF_FARMS, TOKEN_PRICES, STAKING_REWARDS_FARMS
elif NETWORK == "matic":
  from .networks.matic import MASTER_CHEF_FARMS, TOKEN_PRICES, STAKING_REWARDS_FARMS
elif NETWORK == "ethereum":
  from .networks.ethereum import MASTER_CHEF_FARMS, TOKEN_PRICES, STAKING_REWARDS_FARMS

FARM_TVL = Gauge("farm_tvl_dollars", "Farm TVL in dollars", ["network", "project", "staked_token"])
FARM_APR = Gauge("farm_apr_percent", "Farm APR in percent as 0-1.0", ["network", "project", "staked_token"])
PRICE = Gauge("price", "Price of the token on a DEX", ["network", "ticker", "dex"])

def update_prices():
  for dex in TOKEN_PRICES:
    router, tokens = TOKEN_PRICES[dex]

    for ticker, address in tokens:
      try:
        PRICE.labels(NETWORK, ticker, dex).set(priceOf(interface.ERC20(address), router_address=router))
      except ValueError as e:
        print(f"Error while fetching price of {ticker}")
        traceback.print_exc()

def update_master_chef_farms():
  for farm in MASTER_CHEF_FARMS:
    contract, reward_address_method_name, reward_per_block_method_name, router_address, stake_tokens = MASTER_CHEF_FARMS[farm]

    for stake_token_name, stake_token in stake_tokens:
      try:
        tvl, apy = master_chef.fetch_farm_info(
          contract,
          stake_token,
          reward_address_method_name,
          reward_per_block_method_name,
          3,
          router_address
        )

        FARM_TVL.labels(NETWORK, farm, stake_token_name).set(tvl)
        FARM_APR.labels(NETWORK, farm, stake_token_name).set(apy)
      except ValueError as e:
        print(f"Error while fetching APY for {farm} {stake_token_name}")
        traceback.print_exc()

def update_staking_rewards_farms():
  for farm in STAKING_REWARDS_FARMS:
    router_address, stake_tokens = STAKING_REWARDS_FARMS[farm]

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


def update_metrics():
  while True:
    update_prices()

    update_master_chef_farms()

    update_staking_rewards_farms()

    time.sleep(int(os.environ.get('METRICS_SLEEP_SEC', 15)))

def run():
  threading.Thread(target=update_metrics, name="Metrics", daemon=True).start()
