from functools import lru_cache
from brownie import interface
from python_graphql_client import GraphqlClient

STATS_QUERY = """
query pairAddress($pairAddress: String) {
  pairDayDatas(where: { pairAddress: $pairAddress}, first: 1, orderDirection: desc, orderBy:date) {
    pairAddress
    token0 {
      id
      name
    }
    token1 {
      id
      name
    }
    dailyVolumeUSD
    date
    dailyTxns
    reserveUSD
  }
}
"""

SUBGRAPHS_FROM_FACTORY = {
  "0xA40ec8A93293A3179D4b544239916C1B68cB47B6".lower(): "https://api.thegraph.com/subgraphs/name/sunflowerswap/sunflowerswapv2",
  "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f".lower(): "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2",
  "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac".lower(): "https://api.thegraph.com/subgraphs/name/croco-finance/sushiswap"
}

@lru_cache
def subgraph_for(pair_address):
  pair = interface.UniswapPair(pair_address)
  factory = pair.factory()

  return SUBGRAPHS_FROM_FACTORY.get(str(factory).lower(), None)

def pairStats(pair_address: str):
  subgraph_url = subgraph_for(pair_address)

  if not subgraph_url:
    return {}

  client = GraphqlClient(endpoint=subgraph_url)

  response = client.execute(query=STATS_QUERY, variables={"pairAddress": pair_address})

  if response['data'] and response['data']['pairDayDatas'] and len(response['data']['pairDayDatas']) > 0:
    return response['data']['pairDayDatas'][0]

  return None
