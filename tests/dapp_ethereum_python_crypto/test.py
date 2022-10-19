from web3 import Web3

link="/root/.ethereum/geth.ipc"

web3 = Web3(Web3.IPCProvider(link))

print(web3.isConnected())