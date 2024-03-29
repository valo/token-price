from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app

app = Flask(__name__)

import sys
import logging
import os
from brownie import project, network

log_level = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=log_level)

# Set logging level for some verbose modules
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
logging.getLogger("web3.providers.HTTPProvider").setLevel(logging.WARNING)
logging.getLogger("web3.RequestManager").setLevel(logging.WARNING)

p = project.load()
network.connect(os.environ.get('NETWORK', 'ethereum'))
sys.modules["brownie"].interface = p.interface

from scripts.utils import priceOf, priceOf1InchPair, priceOfUniPair, priceOfCurveLPToken, priceOfCurvePool, homoraV2PositionSize, glpPrice, glpWeight, glpRewards, price_unknown_token, chainlink_oracle_price
from scripts.the_graph import pairStats

@app.route('/price/<address>')
def unknown_price(address):
  return str(price_unknown_token(
      address,
      router=request.args.get("router", "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")
  ))

@app.route('/chainlink_oracle/<address>')
def chainlink_oracle(address):
  return str(chainlink_oracle_price(
      address
  ))

@app.route("/uniswap_pair_stats/<address>")
def uniswap_pair_stats(address):
    result = pairStats(address)

    if result:
        result["dailyFeeAPY"] = float(result["dailyVolumeUSD"]) * 0.003 / float(result["reserveUSD"]) * 365

    return result

@app.route("/homora_v2_position_value/<pos_id>")
def homora_v2_position(pos_id):
    return str(homoraV2PositionSize(
        int(pos_id),
        bank_address=request.args.get("bank_address", "0xba5eBAf3fc1Fcca67147050Bf80462393814E54B"),
        router_address=request.args.get("router", "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")
    ))

@app.route("/glp_weight/<address>/<token>")
def glp_weight(address, token):
    weights = glpWeight(address, token)
    return str(weights)

@app.route("/glp/rewards/<rewards_tracker>/claimable/<address>")
def glp_rewards(rewards_tracker, address):
    return str(glpRewards(rewards_tracker, address))

if os.environ.get('RUN_METRICS', '0') == '1':
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })
    import scripts.metrics as metrics
    metrics.run()

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))

  app.run(host = '0.0.0.0', port = port)
