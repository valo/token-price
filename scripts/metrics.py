import threading
import time
from prometheus_client import Gauge
from scripts.utils import priceOf

TOKEN_PRICES = [
  (
    Gauge("ethereum_price", "Ethereum price from Uniswap"),
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
  ),
  (
    Gauge("bitcoin_price", "Bitcoin price from Uniswap"),
    "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
    "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
  ),
]

def update_metrics(project):
  while True:
    for gauge, address, router in TOKEN_PRICES:
      gauge.set(priceOf(project.interface.ERC20(address), router_address=router))

    time.sleep(15)


def run(project):
  threading.Thread(target=update_metrics, name="Metrics", args=[project], daemon=True).start()
