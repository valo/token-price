from scripts.utils import priceOf
from brownie import interface
from .utils import priceOfUniPair, priceOf

ONE_DAY = 86400

def fetch_farm_info(
  stacking_contract,
  router_address):

  reward_token = interface.IERC20(stacking_contract.rewardsToken())

  reward_token_price = priceOf(reward_token, router_address)

  reward_per_day = stacking_contract.rewardRate() * ONE_DAY / 10 ** reward_token.decimals()
  
  stake_token = interface.UniswapPair(stacking_contract.stakingToken())

  stake_token_price = priceOfUniPair(stake_token, router_address)

  tvl = stake_token_price * stake_token.balanceOf(stacking_contract) / 10 ** stake_token.decimals()

  apr = reward_per_day * 365 * reward_token_price / tvl

  return (tvl, apr)
