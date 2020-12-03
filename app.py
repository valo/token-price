from dotenv import load_dotenv
load_dotenv()

from flask import Flask
app = Flask(__name__)

import sys
from brownie import project, network
p = project.load()
network.connect("mainnet")
sys.modules["brownie"].interface = p.interface

from scripts.utils import priceOf, priceOfUniPair

@app.route('/token_price/<address>')
def token_price(address):
    return str(priceOf(p.interface.ERC20(address)))

@app.route('/uniswap_pair_price/<address>')
def uniswap_pair_price(address):
    return str(priceOfUniPair(p.interface.UniswapPair(address)))
