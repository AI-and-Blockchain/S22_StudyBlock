import json
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn, wait_for_confirmation

# Plan to adapt the Custom Asset Problem from lab 2 to fit the criteria for StudyBlock
# Below is base skeleton code for transactions of StudyBlock assets


# Setup HTTP client w/guest key provided by PureStake
algod_address = 'https://testnet-algorand.api.purestake.io/ps2'
algod_token = ""
headers = {
    "X-API-Key": "temp",
}

account_secret_key = "temp"
account_public_key = "temp"

# Initialize an algod client
algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address, headers=headers)

#   Utility function used to print created asset for account and assetid
def print_created_asset(algodclient, account, assetid):    
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'account_info['created-assets'][0] to get info on the created asset
    account_info = algodclient.account_info(account)
    idx = 0;
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1       
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break

#   Utility function used to print asset holding for account and assetid
def print_asset_holding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1        
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break

print("Account 1 address: {}".format(account_public_key))

# CREATE ASSET
# Get network params for transactions before every transaction.
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
params.fee = 1
params.flat_fee = False

# Account 1 creates an asset called latinum and
# sets Account 2 as the manager, reserve, freeze, and clawback address.
# Asset Creation transaction

txn = AssetConfigTxn(
    sender=account_public_key,
    sp=params,
    total=100,
    default_frozen=False,
    unit_name="StudyBlock",
    asset_name="StudyBlock",
    manager=account_public_key,
    reserve=account_public_key,
    freeze=account_public_key,
    clawback=account_public_key,
    url="https://path/to/my/asset/details", 
    decimals=0)

# # Sign with secret key of creator
stxn = txn.sign(account_secret_key)

# Send the transaction to the network and retrieve the txid.
txid = algod_client.send_transaction(txn=stxn)
print(txid)

# Retrieve the asset ID of the newly created asset by first
# ensuring that the creation transaction was confirmed,
# then grabbing the asset id from the transaction.

# Wait for the transaction to be confirmed
wait_for_confirmation(algod_client, txid)

try:
    # Pull account info for the creator
    # account_info = algod_client.account_info(accounts[1]['pk'])
    # get asset_id from tx
    # Get the new asset's information from the creator account
    ptx = algod_client.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]
    print_created_asset(algod_client, account_public_key, asset_id)
    print_asset_holding(algod_client, account_public_key, asset_id)
except Exception as e:
    print(e)
