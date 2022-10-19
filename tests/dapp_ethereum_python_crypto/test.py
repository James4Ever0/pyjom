from web3 import Web3

link="/root/.ethereum/geth.ipc"

web3 = Web3(Web3.IPCProvider(link))

print(web3.isConnected())

account_genesis = "0xde478bde26d711414fae26133e759d8a82a202ab"
# you've connect ethereum to mainnet! not good.

# anyway, we need money!