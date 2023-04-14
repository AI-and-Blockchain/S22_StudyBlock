# 1.4.0 update to add flat-fee=True to avoid bug in the SDK
# In 1.4.0 it is no longer necessary to declare the content type of the send_transaction
# headers={'content-type': 'application/x-binary'}

import json
import time
import base64
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction

# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print('Waiting for confirmation')
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print('Transaction confirmed in round', txinfo.get('confirmed-round'))
    return txinfo

def send_message(message, sender_pub, sender_priv, receiver):
    # Setup HTTP client w/guest key provided by PureStake
    algod_address = 'https://testnet-algorand.api.purestake.io/ps2'
    algod_token = ""
    headers = {
        "X-API-Key": "1xxSTImRIS7YrSc6GQeTc1XILcoh8faP5F3o1rVA",
    }

    account_private_key = sender_priv
    account_public_key = sender_pub

    algodclient = algod.AlgodClient(algod_token, algod_address, headers)

    # get suggested parameters from Algod
    params = algodclient.suggested_params()

    gh = params.gh
    first_valid_round = params.first
    last_valid_round = params.last
    fee = params.min_fee
    send_amount = 0
    note = message

    existing_account = account_public_key
    send_to_address = receiver

    # Create and sign transaction
    tx = transaction.PaymentTxn(existing_account, params, send_to_address, send_amount, note=note)
    signed_tx = tx.sign(account_private_key)

    try:
        tx_confirm = algodclient.send_transaction(signed_tx)
        print('Transaction sent with ID', signed_tx.transaction.get_txid())
        wait_for_confirmation(algodclient, txid=signed_tx.transaction.get_txid())
    except Exception as e:
        print(e)

send_message("Hi_TEST", "2W4PBQN3ZTAG54D3MM2CJDLN4WTDTQJVV2W4AHO7SHYOSDIDWV6HM2B3KM", "L+ds9q28iYcsgeu/5BOX8ZSHd4KUup2q4/SutqLeCDPVuPDBu8zAbvB7YzQkjW3lpjnBNa6twB3fkfDpDQO1fA==", 'BU5IN3BOIYVWD3TW2XQFOQJ3EGFFYCMHN24JBNMR5IU2LWST74TPZAQYBI')