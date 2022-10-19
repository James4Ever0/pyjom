from web3 import Web3

link="/root/.ethereum/geth.ipc"

web3 = Web3(Web3.IPCProvider(link))

print(web3.isConnected())

# account = "0x90316d605bbe3e8caa2bb90f5d63a35dbfada842"
# you've connect ethereum to mainnet! not good.

# anyway, we need money!