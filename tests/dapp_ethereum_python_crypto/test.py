from web3 import Web3

# https://hackernoon.com/hands-on-creating-your-own-local-private-geth-node-beginner-friendly-3d45902cc612
link = "/root/.ethereum/geth.ipc"

web3 = Web3(Web3.IPCProvider(link))

print(web3.isConnected())

account_genesis = "0xde478bde26d711414fae26133e759d8a82a202ab"  # aka: eth.coinbase
password_genesis = "abcdefg"
# let's see!

target_account = "0x033799af9b29e1d7dbf3c8dd64647df345f67bf1"

# you was connected ethereum to mainnet! not good.

# anyway, we need money!

b = web3.eth.get_balance(web3.eth.coinbase)
print(b)
# proof of authority, puppeth

## need password!
web3.eth.
web3.eth.send_transaction(
    {
        "to": Web3.toChecksumAddress(target_account),
        "from": web3.eth.coinbase,
        "value": 12345,
    }
)


b = web3.eth.get_balance(target_account)
print(b)
