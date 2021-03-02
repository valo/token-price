from brownie import interface
from prometheus_client import Gauge

QUICKSWAP_ROUTER = "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff"

USDC_WETH_STACKING = interface.StakingRewards("0x9732E1cC876d8D0B61389385fC1FC756920404fd")
DAI_WETH_STACKING = interface.StakingRewards("0xDFc1b89b6184DfCC7371E3dd898377ECBFEf7058")

MATIC_USDC = interface.IERC20("0x2791bca1f2de4661ed88a30c99a7a9449aa84174")
MATIC_ETH = interface.IERC20("0x7ceb23fd6bc0add59e62ac25578270cff1b9f619")
MATIC_BTC = interface.IERC20("0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6")

TOKEN_PRICES = [
  (
    Gauge("price_ethereum", "Ethereum price from Uniswap", ["network"]),
    MATIC_ETH,
    QUICKSWAP_ROUTER
  ),
  (
    Gauge("price_bitcoin", "Bitcoin price from Uniswap", ["network"]),
    MATIC_BTC,
    QUICKSWAP_ROUTER
  ),
]

MASTER_CHEF_FARMS = {
}

STACKING_REWARDS_FARMS = {
  "QuickSwap": (
    QUICKSWAP_ROUTER,
    [
      ("USDC_ETH", USDC_WETH_STACKING),
      ("DAI_ETH", DAI_WETH_STACKING),
    ]
  ),
}
