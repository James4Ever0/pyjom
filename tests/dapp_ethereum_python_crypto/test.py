from web3 import Web3

# https://hackernoon.com/hands-on-creating-your-own-local-private-geth-node-beginner-friendly-3d45902cc612
link = "/root/.ethereum/geth.ipc"

web3 = Web3(Web3.IPCProvider(link))

print(web3.isConnected())

account_genesis = "0xde478bde26d711414fae26133e759d8a82a202ab"  # aka: eth.coinbase
account_genesis = Web3.toChecksumAddress(account_genesis)
password_genesis = "abcdefg"
# let's see!

target_account = "0x033799af9b29e1d7dbf3c8dd64647df345f67bf1"
target_account = Web3.toChecksumAddress(target_account)
# you was connected ethereum to mainnet! not good.

# anyway, we need money!

b = web3.eth.get_balance(web3.eth.coinbase)
print(b)
# proof of authority, puppeth

## need password!
web3.geth.personal.unlock_account(web3.eth.coinbase, password_genesis)
web3.eth.send_transaction(
    {
        "to": target_account,
        "from": web3.eth.coinbase,
        "value": 1,
    }
)
web3.geth.personal.lock_account(web3.eth.coinbase)
# you can choose to use 'with' statement.


b = web3.eth.get_balance(target_account)
print(b)

# still no money! fuck.
