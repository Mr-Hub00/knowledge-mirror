import os
from web3 import Web3

def get_eth_web3():
    rpc = os.getenv("ETH_RPC_URL", "")
    return Web3(Web3.HTTPProvider(rpc)) if rpc else None