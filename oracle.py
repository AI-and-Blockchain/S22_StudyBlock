import cx_Oracle
from algosdk.v2client import algod
from algosdk import transaction

# Set the Oracle database connection details
username = "your_username"
password = "your_password"
database_name = "your_database_name"

# Set the Algorand API connection details
purestake_key = "4wiTzNyn5x4zVI46Vq5Y392lLhlgh8j7hNmHkMX7"
endpoint_address = "https://testnet-algorand.api.purestake.io/ps2"
purestake_header = {'X-Api-key': purestake_key}
client = algod.AlgodClient(purestake_key, endpoint_address, headers=purestake_header)

# Define the Algorand addresses and private keys
sender_address = "SENDER_ADDRESS"
sender_private_key = "SENDER_PRIVATE_KEY"
receiver_address = "RECEIVER_ADDRESS"
receiver_private_key = "RECEIVER_PRIVATE_KEY"

# Define the amount of Algos to transfer
algos_amount = 10000

# Define the data to transfer
data = "hello, receiver!"

# Define the price of the data
data_price = 5000

# Create the connection object
connection = cx_Oracle.connect(username, password, database_name)

# Create a cursor object
cursor = connection.cursor()

# Execute a query to retrieve the patient data
patient_id = "12345"
cursor.execute("SELECT * FROM patient_data WHERE id = :id", {'id': patient_id})
patient_data = cursor.fetchone()

# Close the cursor and the connection
cursor.close()
connection.close()

# Get suggested parameters for the transaction
params = client.suggested_params()

# Create the atomic transfer transaction
txn_1 = transaction.PaymentTxn(
    sender=sender_address,
    receiver=receiver_address,
    amt=algos_amount,
    sp=params,
)

txn_2 = transaction.ApplicationNoOpTxn(
    sender=sender_address,
    sp=params,
    app_args=[bytes(patient_data, "utf-8")],
)

txn_3 = transaction.PaymentTxn(
    sender=receiver_address,
    receiver=sender_address,
    amt=data_price,
    sp=params,
)

# Group the transactions together in an atomic transfer group
group_id = transaction.calculate_group_id([txn_1, txn_2, txn_3])
txn_1.group = group_id
txn_2.group = group_id
txn_3.group = group_id

# Sign the transactions with the private keys
signed_txn_1 = txn_1.sign(sender_private_key)
signed_txn_2 = txn_2.sign(sender_private_key)
signed_txn_3 = txn_3.sign(receiver_private_key)

# Submit the transactions to the Algorand network
txns = [signed_txn_1, signed_txn_2, signed_txn_3]
tx_id = client.send_transactions(txns)

# Wait for the transactions to be confirmed
client.wait_for_confirmation(tx_id)
