from brownie import interface
from functools import lru_cache

TRADERJOE_ROUTER = "0x60aE616a2155Ee3d9A68541Ba4544862310933d4"
PANGOLIN_ROUTER = "0xE54Ca86531e17Ef3616d22Ca28b0D458b6C89106"

ETH = interface.IERC20("0x49D5c2BdFfac6CE2BFdB6640F4F80f226bc10bAB")
BTC = interface.IERC20("0x50b7545627a5162f82a992c33b87adc75187b218")
USDC = interface.IERC20("0xA7D7079b0FEaD91F3e65f86E8915Cb59c1a4C664")
USDT = interface.IERC20("0xc7198437980c041c805a1edcba50c1ce5db95118")
DAI = interface.IERC20("0xd586e7f844cea2f87f50152665bcbc2c279d8d70")
TIME = interface.IERC20("0xb54f16fb19478766a268f172c9480f8da1a7c9c3")
AVAX = interface.IERC20("0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7")
crvUSDBTCETH = interface.CurveLPToken("0x1daB6560494B04473A0BE3E7D83CF3Fdf3a51828")

tVaultUSDC = interface.yEarnVault("0x52cE2c4Bd817AdB765c476901cc09621DCACEc62")
tVaultDAI = interface.yEarnVault("0xdC808bADe323205f2c794198C1adDa8aEF215E29")
tVaultAVAX = interface.yEarnVault("0x83EA27549acc3CB64c3fCda8379d1eA229a02712")
tVaultETH = interface.yEarnVault("0x7f99CC27EF01F0d32939dBd993f6a857B6e9d235")
tVaultBTC = interface.yEarnVault("0x4AaC7D14E674BCE476eD387FF5abb0Ac3F3187a1")
tVault3crypto_V2 = interface.yEarnVault("0x71712Ad47b2cBC4Fb2e814dBaC44A31749A5195e")

@lru_cache()
def TOKEN_PRICES():
  return {
  "TraderJoe": (
    TRADERJOE_ROUTER,
    [
      ("WETH.e", ETH),
      ("WBTC.e", BTC),
      ("USDC.e", USDC),
      ("USDT.e", USDT),
      ("DAI.e", DAI),
      ("TIME", TIME),
      ("crvUSDBTCETH", crvUSDBTCETH),

      ("tvUSDC.e", tVaultUSDC),
      ("tvDAI.e", tVaultDAI),
      ("tvWBTC.e", tVaultBTC),
      ("tvWETH.e", tVaultETH),
      ("tvWAVAX", tVaultAVAX),
      ("tvcrvUSDBTCETH", tVault3crypto_V2),
    ]
  ),
  "Pangolin": (
    PANGOLIN_ROUTER,
    [
      ("AVAX", AVAX),
    ]
  ),
}

def MASTER_CHEF_FARMS():
  return {}

def STAKING_REWARDS_FARMS():
  return {}

ADDRESS_BALANCES = []
