import threading
import time
import os
import traceback
from brownie import interface, Contract
from prometheus_client import Gauge
from scripts.utils import priceOf
from . import master_chef
from .utils import priceOf, priceOfUniPair

VIKING_MASTER_CHEF = interface.VikingMasterChef("0xEf6e807fD2c0Ef5883A03Ed1b962333E8C9b725f")
OATSWAP_MASTER_CHEF = interface.OatMasterChef("0x96aA7C001576a7C581Ef01655f34B674d4D17de1")
ICECREAM_MASTER_CHEF = interface.IceCreamMasterChef("0xC26316b19117495E89c187339Ddb6E86f1e39f0c")
GOOSE_MASTER_CHEF = interface.GooseMasterChef("0xe70E9185F5ea7Ba3C5d63705784D8563017f2E57")
SLIME_MASTER_CHEF = interface.SlimeMasterChef("0x4B0073A79f2b46Ff5a62fA1458AAc86Ed918C80C")

PANCAKE_USDT_BUSD = interface.UniswapPair("0xc15fa3e22c912a276550f3e5fe3b0deb87b55acd")
PANCAKE_DAI_BUSD = interface.UniswapPair("0x3ab77e40340ab084c3e23be8e5a6f7afed9d41dc")
PANCAKE_USDC_BUSD = interface.UniswapPair("0x680dd100e4b394bda26a59dd5c119a391e747d18")
PANCAKE_VAI_BUSD = interface.UniswapPair("0xff17ff314925dff772b71abdff2782bc913b3575")
PANCAKE_UST_BUSD = interface.UniswapPair("0xd1f12370b2ba1c79838337648f820a87edf5e1e6")
PANCAKE_BNB_BUSD = interface.UniswapPair("0x1b96b92314c44b159149f7e0303511fb2fc4774f")
PANCAKE_BNB_BTC = interface.UniswapPair("0x7561eee90e24f3b348e1087a005f78b4c8453524")
PANCAKE_BNB_ETH = interface.UniswapPair("0x70d8929d04b60af4fb9b58713ebcf18765ade422")


PANCAKE_OAT_BUSD = interface.UniswapPair("0xbfe20f5a8851b536e68551ab8cb1768aa0627d31")
PANCAKE_OAT_BNB = interface.UniswapPair("0x58f503ba111089507ee7cfec4a826463981d2ab2")

PANCAKE_VIKING_BUSD = interface.UniswapPair("0x9b989a7b8963f4b08ec094710e2966fb3c7f6c43")
PANCAKE_VIKING_BNB = interface.UniswapPair("0xc79173e5f6501d7c1ab2f4e7544b13fc6562ce6a")

PANCAKE_EGG_BUSD = interface.UniswapPair("0x19e7cbecdd23a16dfa5573df54d98f7caae03019")
PANCAKE_EGG_BNB = interface.UniswapPair("0xd1b59d11316e87c3a0a069e80f590ba35cd8d8d3")

PANCAKE_SLME_BUSD = interface.UniswapPair("0xfbd0b87f4132e5a14aa85c21476738c0c13fd06c")
PANCAKE_SLME_BNB = interface.UniswapPair("0xcb645714520080ef4e65de3254d61356262f0818")

PANCAKESWAP_ROUTER = "0x05ff2b0db69458a0750badebc4f9e13add608c7f"

ICECREAM_USDT_BUSD = interface.UniswapPair("0x57Bcf3Bb68f6E8DF00b9e6AD6aF8cE58fe7FC350")
ICECREAM_BUSD_BNB = interface.UniswapPair("0x875DfffcBd97f6C7038E97A4959B0590C8714e1c")
ICECREAM_ETH_BNB = interface.UniswapPair("0x68c277E93D9EB923E2EA9bfFC643307E731C044f")
ICECREAMSWAP_ROUTER = "0x6728f3c8241C44Cc741C9553Ff7824ba9E932A4A"

BSC_DAI = interface.IERC20("0x1af3f329e8be154074d8769d1ffa4ee058b1dbc3")
BSC_BUSD = interface.IERC20("0xe9e7cea3dedca5984780bafc599bd69add087d56")
BSC_USDT = interface.IERC20("0x55d398326f99059ff775485246999027b3197955")
BSC_USDC = interface.IERC20("0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d")
BSC_VAI = interface.IERC20("0x4bd17003473389a42daf6a0a729f6fdb328bbbd7")
BSC_ETH = interface.IERC20("0x2170ed0880ac9a755fd29b2688956bd959f933f8")
BSC_BTC = interface.IERC20("0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c")
BSC_BNB = interface.IERC20("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")

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

MASTER_CHEF_FARMS = {
  "Viking": (
    VIKING_MASTER_CHEF,
    "viking",
    "vikingPerBlock",
    PANCAKESWAP_ROUTER,
    [
      ("VIKING_BUSD", PANCAKE_VIKING_BUSD),
      ("VIKING_BNB", PANCAKE_VIKING_BNB),
      ("USDT_BUSD", PANCAKE_USDT_BUSD),
      ("DAI_BUSD", PANCAKE_DAI_BUSD),
      ("USDC_BUSD", PANCAKE_USDC_BUSD),
      ("BUSD", BSC_BUSD),
      ("DAI", BSC_DAI),
      ("USDT", BSC_USDT),
      ("USDC", BSC_USDC),
      ("ETH", BSC_ETH),
      ("BTC", BSC_BTC),
    ]
  ),
  "OatSwap": (
    OATSWAP_MASTER_CHEF,
    "oat",
    "oatPerBlock",
    PANCAKESWAP_ROUTER,
    [
      ("OAT_BUSD", PANCAKE_OAT_BUSD),
      ("OAT_BNB", PANCAKE_OAT_BNB),
      ("USDT_BUSD", PANCAKE_USDT_BUSD),
      ("DAI_BUSD", PANCAKE_DAI_BUSD),
      ("USDC_BUSD", PANCAKE_USDC_BUSD),
      ("VAI_BUSD", PANCAKE_VAI_BUSD),
      ("UST_BUSD", PANCAKE_UST_BUSD),
      ("BNB_BUSD", PANCAKE_BNB_BUSD),
      ("BNB_ETH", PANCAKE_BNB_ETH),
      ("BNB_BTC", PANCAKE_BNB_BTC),
      ("BUSD", BSC_BUSD),
      ("DAI", BSC_DAI),
      ("USDT", BSC_USDT),
      ("USDC", BSC_USDC),
      ("VAI", BSC_VAI),
      ("ETH", BSC_ETH),
      ("BTC", BSC_BTC),
      ("BNB", BSC_BNB),
    ]
  ),
  "IceCream": (
    ICECREAM_MASTER_CHEF,
    "cream",
    "creamPerBlock",
    ICECREAMSWAP_ROUTER,
    [
      ("USDT_BUSD", ICECREAM_USDT_BUSD),
      ("BUSD_BNB", ICECREAM_BUSD_BNB),
      ("ETH_BNB", ICECREAM_ETH_BNB),
    ]
  ),
  "GooseDefi": (
    GOOSE_MASTER_CHEF,
    "egg",
    "eggPerBlock",
    PANCAKESWAP_ROUTER,
    [
      ("EGG_BUSD", PANCAKE_EGG_BUSD),
      ("EGG_BNB", PANCAKE_EGG_BNB),
      ("USDT_BUSD", PANCAKE_USDT_BUSD),
      ("DAI_BUSD", PANCAKE_DAI_BUSD),
      ("USDC_BUSD", PANCAKE_USDC_BUSD),
      ("BNB_BUSD", PANCAKE_BNB_BUSD),
      ("BNB_ETH", PANCAKE_BNB_ETH),
      ("BNB_BTC", PANCAKE_BNB_BTC),
      ("BUSD", BSC_BUSD),
      ("USDT", BSC_USDT),
      ("DAI", BSC_DAI),
      ("USDC", BSC_USDC),
      ("BTC", BSC_BTC),
      ("ETH", BSC_ETH),
      ("BNB", BSC_BNB),
    ]
  ),
  "Slime": (
    SLIME_MASTER_CHEF,
    "st",
    "slimesPerBlock",
    PANCAKESWAP_ROUTER,
    [
      ("SLME_BUSD", PANCAKE_SLME_BUSD),
      ("SLME_BNB", PANCAKE_SLME_BNB),
      ("USDT_BUSD", PANCAKE_USDT_BUSD),
      ("DAI_BUSD", PANCAKE_DAI_BUSD),
      ("BNB_BUSD", PANCAKE_BNB_BUSD),
      ("BNB_BTC", PANCAKE_BNB_BTC),
      ("BNB_ETH", PANCAKE_BNB_ETH),
      ("BUSD", BSC_BUSD),
      ("USDT", BSC_USDT),
      ("DAI", BSC_DAI),
      ("BTC", BSC_BTC),
      ("ETH", BSC_ETH),
      ("BNB", BSC_BNB),
    ]
  ),
}

def update_metrics():
  while True:
    for gauge, address, router in TOKEN_PRICES:
      try:
        gauge.set(priceOf(interface.ERC20(address), router_address=router))
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

          FARM_TVL.labels(farm, stake_token_name).set(tvl)
          FARM_APR.labels(farm, stake_token_name).set(apy)
        except ValueError as e:
          print(f"Error while fetching APY for {farm} {stake_token_name}")
          traceback.print_exc()

    time.sleep(int(os.environ.get('METRICS_SLEEP_SEC', 15)))


def run():
  threading.Thread(target=update_metrics, name="Metrics", daemon=True).start()
