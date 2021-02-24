from brownie import Contract, interface
from .utils import priceOf

def fetch_farm_info(
  contract,
  stake_token,
  stake_token_price_func,
  reward_address_method_name,
  reward_per_block_method_name,
  block_time,
  router_address):

  points = allocationPoints(contract, stake_token)

  total_allocation_points = contract.totalAllocPoint()

  percent_of_rewards = points / total_allocation_points

  reward_token = interface.IERC20(getattr(contract, reward_address_method_name)())
  reward_token_price = priceOf(reward_token, router_address)

  reward_per_block = getattr(contract, reward_per_block_method_name)() / 10 ** reward_token.decimals()

  stake_token_price = stake_token_price_func(stake_token, router_address)

  tvl = stake_token_price * stake_token.balanceOf(contract) / 10 ** stake_token.decimals()

  apr = 60 / block_time * 60 * 24 * 365 * reward_token_price * percent_of_rewards * reward_per_block / tvl

  return (tvl, apr)
    
def allocationPoints(contract, lp_token):
  total_pools = contract.poolLength()

  for index in range(total_pools):
    info = contract.poolInfo(index)
    current_lp_token, allocation = info[0], info[1]

    if current_lp_token.lower() == lp_token.address.lower():
      return allocation

  return None
