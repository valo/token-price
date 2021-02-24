import threading
import time
import os
from brownie import interface, Contract
from prometheus_client import Gauge
from scripts.utils import priceOf
from . import master_chef
from .utils import priceOf, priceOfUniPair

VIKING_MASTER_CHEF = interface.VikingMasterChef("0xEf6e807fD2c0Ef5883A03Ed1b962333E8C9b725f")
PANCAKE_USDT_BUSD = interface.UniswapPair("0xc15fa3e22c912a276550f3e5fe3b0deb87b55acd")
PANCAKE_DAI_BUSD = interface.UniswapPair("0x3ab77e40340ab084c3e23be8e5a6f7afed9d41dc")
PANCAKE_USDC_BUSD = interface.UniswapPair("0x680dd100e4b394bda26a59dd5c119a391e747d18")
PANCAKESWAP_ROUTER = "0x05ff2b0db69458a0750badebc4f9e13add608c7f"

BSC_DAI = interface.IERC20("0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82")
BSC_BUSD = interface.IERC20("0xe9e7cea3dedca5984780bafc599bd69add087d56")
BSC_USDT = interface.IERC20("0x55d398326f99059ff775485246999027b3197955")
BSC_USDC = interface.IERC20("0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d")
BSC_ETH = interface.IERC20("0x2170ed0880ac9a755fd29b2688956bd959f933f8")
BSC_BTC = interface.IERC20("0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c")

FARM_TVL = Gauge("farm_tvl_dollars", "Farm TVL in dollars", ["project", "staked_token"])
FARM_APR = Gauge("farm_apr_percent", "Farm APR in percent as 0-1.0", ["project", "staked_token"])

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
    ("Viking", "USDT_BUSD"),
    [
      VIKING_MASTER_CHEF,
      PANCAKE_USDT_BUSD,
      priceOfUniPair,
      "viking",
      "vikingPerBlock",
      3,
      PANCAKESWAP_ROUTER
    ]
  ),
  (
    ("Viking", "DAI_BUSD"),
    [
      VIKING_MASTER_CHEF,
      PANCAKE_DAI_BUSD,
      priceOfUniPair,
      "viking",
      "vikingPerBlock",
      3,
      PANCAKESWAP_ROUTER
    ]
  ),
  (
    ("Viking", "USDC_BUSD"),
    [
      VIKING_MASTER_CHEF,
      PANCAKE_USDC_BUSD,
      priceOfUniPair,
      "viking",
      "vikingPerBlock",
      3,
      PANCAKESWAP_ROUTER
    ]
  ),
  (
    ("Viking", "BUSD"),
    [
      VIKING_MASTER_CHEF,
      BSC_BUSD,
      priceOf,
      "viking",
      "vikingPerBlock",
      3,
      PANCAKESWAP_ROUTER
    ]
  ),
  (
    ("Viking", "DAI"),
    [
      VIKING_MASTER_CHEF,
      BSC_DAI,
      priceOf,
      "viking",
      "vikingPerBlock",
      3,
      PANCAKESWAP_ROUTER
    ]
  ),
  (
    ("Viking", "USDT"),
    [
      VIKING_MASTER_CHEF,
      BSC_USDT,
      priceOf,
      "viking",
      "vikingPerBlock",
      3,
      PANCAKESWAP_ROUTER
    ]
  ),
  (
    ("Viking", "USDC"),
    [
      VIKING_MASTER_CHEF,
      BSC_USDC,
      priceOf,
      "viking",
      "vikingPerBlock",
      3,
      PANCAKESWAP_ROUTER
    ]
  ),
  (
    ("Viking", "ETH"),
    [
      VIKING_MASTER_CHEF,
      BSC_ETH,
      priceOf,
      "viking",
      "vikingPerBlock",
      3,
      PANCAKESWAP_ROUTER
    ]
  ),
  (
    ("Viking", "BTC"),
    [
      VIKING_MASTER_CHEF,
      BSC_BTC,
      priceOf,
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

    for labels, args in MASTER_CHEF_FARMS:
      tvl, apy = master_chef.fetch_farm_info(*args)

      FARM_TVL.labels(*labels).set(tvl)
      FARM_APR.labels(*labels).set(apy)

    time.sleep(int(os.environ.get('METRICS_SLEEP_SEC', 15)))


def run():
  threading.Thread(target=update_metrics, name="Metrics", daemon=True).start()
