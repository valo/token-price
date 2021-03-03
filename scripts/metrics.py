import threading
import time
import os
import traceback
from brownie import interface
from prometheus_client import Gauge
from . import master_chef
from . import staking_rewards
from .utils import priceOf

NETWORK = os.environ.get("NETWORK", "bsc")

if NETWORK == "bsc":
  from .networks.bsc import MASTER_CHEF_FARMS, TOKEN_PRICES, STAKING_REWARDS_FARMS
elif NETWORK == "matic":
  from .networks.matic import MASTER_CHEF_FARMS, TOKEN_PRICES, STAKING_REWARDS_FARMS

FARM_TVL = Gauge("farm_tvl_dollars", "Farm TVL in dollars", ["network", "project", "staked_token"])
FARM_APR = Gauge("farm_apr_percent", "Farm APR in percent as 0-1.0", ["network", "project", "staked_token"])

def update_metrics():
  while True:
    for gauge, address, router in TOKEN_PRICES:
      try:
        gauge.labels(NETWORK).set(priceOf(interface.ERC20(address), router_address=router))
      except ValueError as e:
        print(f"Error while fetching price of {gauge._name}")
        traceback.print_exc()

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

    time.sleep(int(os.environ.get('METRICS_SLEEP_SEC', 15)))


def run():
  threading.Thread(target=update_metrics, name="Metrics", daemon=True).start()
