from brownie import interface
from functools import lru_cache

TRADERJOE_ROUTER = "0x60aE616a2155Ee3d9A68541Ba4544862310933d4"

ETH = interface.IERC20("0x49D5c2BdFfac6CE2BFdB6640F4F80f226bc10bAB")
BTC = interface.IERC20("0x50b7545627a5162f82a992c33b87adc75187b218")
USDC = interface.IERC20("0xA7D7079b0FEaD91F3e65f86E8915Cb59c1a4C664")
USDT = interface.IERC20("0xc7198437980c041c805a1edcba50c1ce5db95118")
TIME = interface.IERC20("0xb54f16fb19478766a268f172c9480f8da1a7c9c3")

@lru_cache()
def TOKEN_PRICES():
  return {
  "TraderJoe": (
    TRADERJOE_ROUTER,
    [
      ("ETH", ETH),
      ("BTC", BTC),
      ("TIME", TIME),
    ]
  ),
}

def MASTER_CHEF_FARMS():
  return {}

def STAKING_REWARDS_FARMS():
  return {}

ADDRESS_BALANCES = []
