import requests
import json
import base64
from algosdk.v2client import algod
from algosdk import transaction

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

def show_messages(init_address):
    retlist = []
    # set up query parameters
    address = init_address
    headers = {
        "X-API-Key": "1xxSTImRIS7YrSc6GQeTc1XILcoh8faP5F3o1rVA",
    }

    # construct query URL
    base_url = "https://algoindexer.testnet.algoexplorerapi.io/v2/accounts/"
    query_url = f"{base_url}{address}/transactions"

    # submit query and parse JSON response
    response = requests.get(query_url)
    response_json = json.loads(response.text)

    # process response data
    transactions = response_json["transactions"]

    for tx in transactions:
        if(tx["sender"] == address):
            continue
        if(tx["id"] == '7H6KASJRX6KOXWYNLGGPIQOYH3EU7OPCE4WMYE4M3IBU3HAZ3QSA'):
            continue
        note = "empty"
        if("note" in tx):
            note = tx['note']
            base64_bytes = note.encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('ascii')
            retlist.append([message, tx["sender"]])
    return retlist

def runner(init_address):
    # set up query parameters
    address = init_address
    headers = {
        "X-API-Key": "1xxSTImRIS7YrSc6GQeTc1XILcoh8faP5F3o1rVA",
    }

    # construct query URL
    base_url = "https://algoindexer.testnet.algoexplorerapi.io/v2/accounts/"
    query_url = f"{base_url}{address}/transactions"

    # submit query and parse JSON response
    response = requests.get(query_url)
    response_json = json.loads(response.text)

    # process response data
    transactions = response_json["transactions"]

    for tx in transactions:
        tx_id = tx["id"]
        if(tx_id == '7H6KASJRX6KOXWYNLGGPIQOYH3EU7OPCE4WMYE4M3IBU3HAZ3QSA'):
            continue
        amount = 0
        if("payment-transaction" in tx):
            amount = tx["payment-transaction"]["amount"]
        note = "empty"
        if("note" in tx):
            note = tx['note']
            base64_bytes = note.encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('ascii')
            # do something with tx_id and amount
            if(len(message) > 4 and message[0:4] == 'DATA'):
                # data received 
                sender = tx['sender']
                algodclient = algod.AlgodClient("", 'https://testnet-algorand.api.purestake.io/ps2', headers)
                # get suggested parameters from Algod
                params = algodclient.suggested_params()

                gh = params.gh
                first_valid_round = params.first
                last_valid_round = params.last
                fee = params.min_fee
                send_amount = 10000
                note = "Data received"

                existing_account = address
                send_to_address = sender

                # Create and sign transaction
                tx = transaction.PaymentTxn(existing_account, params, send_to_address, send_amount, note=note)
                signed_tx = tx.sign('hoiaCAyWuMsTSm84Jl12Rx/M7Lae4yZTqImk3zUPE2MNOobsLkYrYe521eBXQTshilwJh264kLWR6iml2lP/Jg==')

                try:
                    tx_confirm = algodclient.send_transaction(signed_tx)
                    # print('Transaction sent with ID', signed_tx.transaction.get_txid())
                    wait_for_confirmation(algodclient, txid=signed_tx.transaction.get_txid())
                except Exception as e:
                    print(e)

        # print(tx_id, amount, message)
        message = 'empty'

# runner("BU5IN3BOIYVWD3TW2XQFOQJ3EGFFYCMHN24JBNMR5IU2LWST74TPZAQYBI")
