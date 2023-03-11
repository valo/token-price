import os
import cachetools.func
from brownie import interface

DEFAULT_TTL_CACHE=60

@cachetools.func.ttl_cache(ttl=DEFAULT_TTL_CACHE)
def get_usdc_price() -> float:
  oracle = interface.EACAggregatorProxy(
    os.environ.get('USDC_ORACLE_ADDRESS', "0x8fffffd4afb6115b954bd326cbe7b4ba576818f6")
  )

  return oracle.latestRoundData()[1] / 10 ** oracle.decimals()

@cachetools.func.ttl_cache(ttl=DEFAULT_TTL_CACHE)
def get_usdt_price() -> float:
  oracle = interface.EACAggregatorProxy(
    os.environ.get('USDT_ORACLE_ADDRESS', "0x3e7d1eab13ad0104d2750b8863b489d65364e32d")
  )

  return oracle.latestRoundData()[1] / 10 ** oracle.decimals()
