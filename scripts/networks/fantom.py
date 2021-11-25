from brownie import interface
from functools import lru_cache

SPOOKYSWAP_ROUTER = "0xF491e7B69E4244ad4002BC14e878a34207E38c29"

@lru_cache()
def TOKEN_PRICES():
  CRV_TRICRYPTO = interface.CurveLPToken("0x58e57ca18b7a47112b877e31929798cd3d703b0f")

  return {
  "SpookySwap": (
    SPOOKYSWAP_ROUTER,
    [
      ("crvTricrypto", CRV_TRICRYPTO),
    ]
  ),
}

def MASTER_CHEF_FARMS():
  return {}

def STAKING_REWARDS_FARMS():
  return {}

ADDRESS_BALANCES = []
