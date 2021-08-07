from brownie import interface
from functools import lru_cache

UNISWAP_ROUTER = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
SUSHISWAP_ROUTER = "0xd9e1ce17f2641f24ae83637ab66a2cca9c378b9f"

ETH = interface.IERC20("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
BTC = interface.IERC20("0x2260fac5e5542a773aa44fbcfedf7c193bc2c599")
UNI = interface.IERC20("0x1f9840a85d5af5bf1d1762f925bdaddc4201f984")
SUSHI = interface.IERC20("0x6b3595068778dd592e39a122f4f5a5cf09c90fe2")
YFI = interface.IERC20("0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e")
USDC = interface.IERC20("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
USDT = interface.IERC20("0xdac17f958d2ee523a2206206994597c13d831ec7")
AAVE = interface.IERC20("0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9")

@lru_cache()
def TOKEN_PRICES():
  ONE_INCH = interface.IERC20("0x111111111117dc0aa78b770fa6a738034120c302")
  DAI = interface.IERC20("0x6b175474e89094c44da98b954eedeac495271d0f")
  BUSD = interface.IERC20("0x4fabb145d64652a948d72533023f6e7a623c7c53")
  UWL = interface.IERC20("0xdbdd6f355a37b94e6c7d32fef548e98a280b8df5")
  COMP = interface.IERC20("0xc00e94cb662c3520282e6f5717214004a7f26888")
  LRC = interface.IERC20("0xbbbbca6a901c926f240b89eacb641d8aec7aeafd")
  LQTY = interface.IERC20("0x6dea81c8171d0ba574754ef6f8b412f2ed88c54d")
  LUSD = interface.IERC20("0x5f98805a4e8be255a32880fdec7f6728c6568ba0")

  UNI_FRAX_ETH = interface.UniswapPair("0xFD0A40Bc83C5faE4203DEc7e5929B446b07d1C76")
  UNI_LUSD_ETH = interface.UniswapPair("0xf20ef17b889b437c151eb5ba15a47bfc62bff469")
  UNI_USDT_ETH = interface.UniswapPair("0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852")
  UNI_USDC_ETH = interface.UniswapPair("0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc")

  SUSHI_ALPHA_ibETHv2 = interface.UniswapPair("0xf79a07cd3488bbafb86df1bad09a6168d935c017")
  SUSHI_ALCX_ETH = interface.UniswapPair("0xc3f279090a47e80990fe3a9c30d24cb117ef91a8")
  SUSHI_bDPI_ETH = interface.UniswapPair("0x8d782C5806607E9AAFB2AC38c1DA3838Edf8BD03")
  SUSHI_USDC_ETH = interface.UniswapPair("0x397ff1542f962076d0bfe58ea045ffa2d347aca0")
  SUSHI_USDT_ETH = interface.UniswapPair("0x06da0fd433c1a5d7a4faa01111c044910a184553")

  SUSHI_ALCX = interface.IERC20("0xdbdb4d16eda451d0503b854cf79d55697f90c8df")
  SUSHI_ANY = interface.IERC20("0xf99d58e463a2e07e5692127302c20a191861b4d6")

  CRV_TRICRYPTO = interface.CurveLPToken("0xca3d75ac011bf5ad07a98d02f18225f9bd9a6bdf")
  CRV_TRICRYPTO2 = interface.CurveLPToken("0xc4AD29ba4B3c580e6D59105FFf484999997675Ff")
  yvCRV_TRICRYPTO = interface.yEarnVault("0x3d980e50508cfd41a13837a60149927a11c03731")

  return {
  "Uniswap": (
    UNISWAP_ROUTER,
    [
      ("ETH", ETH),
      ("BTC", BTC),
      ("UNI", UNI),
      ("SUSHI", SUSHI),
      ("1INCH", ONE_INCH),
      ("YFI", YFI),
      ("DAI", DAI),
      ("USDC", USDC),
      ("USDT", USDT),
      ("BUSD", BUSD),
      ("LUSD", LUSD),
      ("UWL", UWL),
      ("COMP", COMP),
      ("LRC", LRC),
      ("AAVE", AAVE),
      ("LQTY", LQTY),
      ("FRAX_ETH", UNI_FRAX_ETH),
      ("LUSD_ETH", UNI_LUSD_ETH),
      ("USDT_ETH", UNI_USDT_ETH),
      ("USDC_ETH", UNI_USDC_ETH),
      ("crvTricrypto", CRV_TRICRYPTO),
      ("crvTricrypto2", CRV_TRICRYPTO2),
      ("yvCurve-triCrypto", yvCRV_TRICRYPTO),
    ]
  ),
  "SushiSwap": (
    SUSHISWAP_ROUTER,
    [
      ("ALPHA_ibETHv2", SUSHI_ALPHA_ibETHv2),
      ("ALCX", SUSHI_ALCX),
      ("ANY", SUSHI_ANY),
      ("ALCX_ETH", SUSHI_ALCX_ETH),
      ("bDPI_ETH", SUSHI_bDPI_ETH),
      ("USDC_ETH", SUSHI_USDC_ETH),
      ("USDT_ETH", SUSHI_USDT_ETH),
    ]
  ),
}

def MASTER_CHEF_FARMS():
  return {}

def STAKING_REWARDS_FARMS():
  return {}
