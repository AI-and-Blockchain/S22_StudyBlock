import requests
import json

# set up query parameters
address = "BU5IN3BOIYVWD3TW2XQFOQJ3EGFFYCMHN24JBNMR5IU2LWST74TPZAQYBI"
limit = 100
after_time = 1648454400

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
    amount = 0
    if("payment-transaction" in tx):
        amount = tx["payment-transaction"]["amount"]
    note = "empty"
    if("note" in tx):
        note = tx['note']
    # do something with tx_id and amount
    print(tx_id, amount, note)

