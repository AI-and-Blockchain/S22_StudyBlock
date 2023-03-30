import json
from pyteal import *
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
# Define the smart contract for the patient recruitment system
# This smart contract is written in TEAL, Algorand's smart contract programming language

# Global Variables
register = Bytes("register")
patient = Bytes("patient")
trial_id = Bytes("trial ID")
patient_id = Bytes("patient ID")
patient_name = Bytes("patient name")
patient_age = Bytes("patient age")
patient_gender = Bytes("patient gender")
data_sharing = Bytes("data-sharing")
data = Bytes("data")

# Register a new patient
# This function is called when the "register" parameter is passed to the smart contract
# It registers the patient information in a hash table and assigns the patient an ID
register_patient = And(
    Txn.application_args[0] == register,
    App.globalPut(
        Bytes("patients"),
        Txn.application_args[2],
        {
            patient_id: Txn.application_args[3],
            trial_id: Txn.application_args[1],
            patient_name: Txn.application_args[4],
            patient_age: Txn.application_args[5],
            patient_gender: Txn.application_args[6],
        },
    ),
)

# Data sharing
# This function is called when the "data-sharing" parameter is passed to the smart contract
# It allows patients to share their data with the clinical trial program
share_data = And(
    Txn.application_args[0] == data_sharing,
    App.globalPut(
        Txn.application_args[2],
        Txn.application_args[1],
        Txn.application_args[3],
    ),
)

# Token rewards
# This function is called when a patient completes a task or milestone in the clinical trial
# It rewards the patient with tokens, which can be used as an incentive to participate in the trial
token_rewards = And(
    Txn.application_args[0] == data,
    App.globalPut(
        Txn.application_args[1],
        Txn.application_args[4],
        App.globalGet(Txn.application_args[1], Txn.application_args[4]) + Txn.application_args[2],
    ),
)

# Define the main function
def approval_program():
    return And(
        Or(register_patient, share_data, token_rewards),
        Txn.application_id() == Int(1234567890), # Replace with your application ID
    )

# Define the clear state function
def clear_state_program():
    return Return(Int(1))
