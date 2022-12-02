from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app

app = Flask(__name__)

import sys
import os
from brownie import project, network
p = project.load()
network.connect(os.environ.get('NETWORK', 'ethereum'))
sys.modules["brownie"].interface = p.interface

from scripts.utils import priceOf, priceOf1InchPair, priceOfUniPair, priceOfCurveLPToken, homoraV2PositionSize, glpPrice, glpWeight
from scripts.the_graph import pairStats

@app.route('/token_price/<address>')
def token_price(address):
    return str(priceOf(
        p.interface.IERC20(address),
        router_address=request.args.get("router", "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")
    ))

@app.route('/uniswap_pair_price/<address>')
def uniswap_pair_price(address):
    return str(priceOfUniPair(
        p.interface.UniswapPair(address),
        router_address=request.args.get("router", "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")
    ))

@app.route('/1inch_pair_price/<address>')
def oneinch_pair_price(address):
    return str(priceOf1InchPair(
        p.interface.IMooniswap(address),
        router_address=request.args.get("router", "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")
    ))

@app.route('/yearn_vault_price/<address>')
def yearn_vault_price(address):
    yearn_vault = p.interface.yEarnVault(address)
    return str(yearn_vault.pricePerShare() / 10 ** 18)

@app.route('/curve_lp_price/<address>')
def curve_lp_price(address):
    lp_token = p.interface.CurveLPToken(address)
    return str(priceOfCurveLPToken(
        lp_token,
        router_address=request.args.get("router", "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")
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

@app.route("/glp_price/<address>")
def glp_price(address):
    return str(glpPrice(address))

@app.route("/glp_weight/<address>/<token>")
def glp_weight(address, token):
    weights = glpWeight(address, token)
    return str(weights)

if os.environ.get('RUN_METRICS', '0') == '1':
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })
    import scripts.metrics as metrics
    metrics.run()

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))

  app.run(host = '0.0.0.0', port = port)
