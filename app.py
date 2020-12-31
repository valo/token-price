from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request
app = Flask(__name__)

import sys
from brownie import project, network
p = project.load()
network.connect("mainnet")
sys.modules["brownie"].interface = p.interface

from scripts.utils import priceOf, priceOf1InchPair, priceOfUniPair
from scripts.the_graph import pairStats

@app.route('/token_price/<address>')
def token_price(address):
    return str(priceOf(
        p.interface.ERC20(address),
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
        p.interface.Mooniswap(address),
        router_address=request.args.get("router", "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")
    ))

@app.route("/uniswap_pair_stats/<address>")
def uniswap_pair_stats(address):
    result = pairStats(address)

    if result:
        result["dailyFeeAPY"] = float(result["dailyVolumeUSD"]) * 0.003 / float(result["reserveUSD"]) * 365

    return result
