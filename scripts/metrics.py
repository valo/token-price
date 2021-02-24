import threading
import time
import os
from brownie import interface, Contract
from prometheus_client import Gauge
from scripts.utils import priceOf
import scripts.master_chef as master_chef

VIKING_MASTER_CHEF = interface.VikingMasterChef("0xEf6e807fD2c0Ef5883A03Ed1b962333E8C9b725f")
PANCAKE_USDT_BUSD = interface.IERC20("0xc15fa3e22c912a276550f3e5fe3b0deb87b55acd")
PANCAKE_DAI_BUSD = interface.IERC20("0x3ab77e40340ab084c3e23be8e5a6f7afed9d41dc")
PANCAKE_USDC_BUSD = interface.IERC20("0x680dd100e4b394bda26a59dd5c119a391e747d18")
PANCAKESWAP_ROUTER = "0x05ff2b0db69458a0750badebc4f9e13add608c7f"

TOKEN_PRICES = [
  (
    Gauge("price_ethereum", "Ethereum price from Uniswap"),
    "0x2170ed0880ac9a755fd29b2688956bd959f933f8",
    PANCAKESWAP_ROUTER
  ),
  (
    Gauge("price_bitcoin", "Bitcoin price from Uniswap"),
    "0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c",
    PANCAKESWAP_ROUTER
  ),
]

MASTER_CHEF_FARMS = [
  (
    (
      Gauge("farm_viking_tvl_usdt_busd", "Viking USDT/BUSD TVL"),
      Gauge("farm_viking_apr_usdt_busd", "Viking USDT/BUSD APR")
    ),
    [
      VIKING_MASTER_CHEF,
      PANCAKE_USDT_BUSD,
      "viking",
      "vikingPerBlock",
      3,
      PANCAKESWAP_ROUTER
    ]
  ),
  (
    (
      Gauge("farm_viking_tvl_dai_busd", "Viking USDT/BUSD TVL"),
      Gauge("farm_viking_apr_dai_busd", "Viking USDT/BUSD APR")
    ),
    [
      VIKING_MASTER_CHEF,
      PANCAKE_DAI_BUSD,
      "viking",
      "vikingPerBlock",
      3,
      PANCAKESWAP_ROUTER
    ]
  ),
  (
    (
      Gauge("farm_viking_tvl_usdc_busd", "Viking USDT/BUSD TVL"),
      Gauge("farm_viking_apr_usdc_busd", "Viking USDT/BUSD APR")
    ),
    [
      VIKING_MASTER_CHEF,
      PANCAKE_USDC_BUSD,
      "viking",
      "vikingPerBlock",
      3,
      PANCAKESWAP_ROUTER
    ]
  ),
]

def update_metrics():
  while True:
    for gauge, address, router in TOKEN_PRICES:
      gauge.set(priceOf(interface.ERC20(address), router_address=router))

    for gauges, args in MASTER_CHEF_FARMS:
      tvl, apy = master_chef.fetch_farm_info(*args)

      gauges[0].set(tvl)
      gauges[1].set(apy)

    time.sleep(15)


def run():
  threading.Thread(target=update_metrics, name="Metrics", daemon=True).start()
