from pyteal import *
from messaging.ClinicalTrialMessaging import ClinicalTrialMessaging
from algosdk.v2client import algod
from algosdk import encoding
from algosdk import transaction

# Algod credentials
purestake_key = "YOUR_ALGOD_API_KEY"
endpoint_address = "https://testnet-algorand.api.purestake.io/ps2"
headers = {"X-API-Key": purestake_key}
client = algod.AlgodClient(purestake_key, endpoint_address, headers=headers)

# Account credentials
oracle_address = "ORACLE_ADDRESS"
oracle_mnemonic = "ORACLE_MNEMONIC"
oracle_private_key = encoding.mnemonic_to_private_key(oracle_mnemonic)
researcher_address = "RESEARCHER_ADDRESS"
researcher_price = 5000

# Atomic contract credentials
contract_address = "CONTRACT_ADDRESS"
contract_private_key = "CONTRACT_PRIVATE_KEY"
contract_receiver = "CONTRACT_RECEIVER"
contract_amount = 10000
contract_data = "CONTRACT_DATA"

# Setup clinical trial messaging
messaging = ClinicalTrialMessaging()

# Define PyTeal program for the oracle
program = Seq([
    App.globalPut(Bytes("oracleLastBlock"), Int(0)),
    While(Txn.type_enum() == Int(1), Seq([
        App.globalPut(Bytes("oracleLastBlock"), Txn.last_valid()),
        If(messaging.message_received(Txn.sender()), Seq([
            # Prepare the transaction group for the atomic transfer
            Txn.sender() == Addr(researcher_address),
            Txn.amount() == Int(researcher_price),
            App.localPut(Bytes("data"), Txn.application_args[0]),
            App.optedIn(Txn.sender(), App.id()),
            App.optedIn(Txn.receiver(), App.id()),

            # Create the payment transaction
            payment_txn = Txn.application_args[1],
            Txn.application_args.length() == Int(2),
            payment_txn.type_enum() == Int(4),
            payment_txn.sender() == Addr(contract_receiver),
            payment_txn.receiver() == Addr(Txn.sender()),
            payment_txn.amount() == Int(contract_amount),
            payment_txn.close_remainder_to() == Global.zero_address(),

            # Create the application transaction
            app_txn = Txn.application_args[0],
            app_txn.type_enum() == Int(5),
            app_txn.on_completion() == OnComplete.NoOp,
            app_txn.accounts[0] == Addr(researcher_address),
            app_txn.accounts[1] == Addr(contract_receiver),
            app_txn.foreign_apps.length() == Int(0),
            app_txn.foreign_assets.length() == Int(0),
            app_txn.app_args[0] == Bytes(contract_data),
            app_txn.app_args[1] == payment_txn.txid(),

            # Sign and submit the transaction group
            payment_txn_bytes = payment_txn.get_obj_for_encoding(),
            app_txn_bytes = app_txn.get_obj_for_encoding(),
            txns = [
                transaction.Transaction.payment(payment_txn_bytes),
                transaction.Transaction.app_call(app_txn_bytes)
            ],
            signed_txns = [
                payment_txn.sign(contract_private_key),
                app_txn.sign(oracle_private_key)
            ],
            txid = client.send_transactions(signed_txns)
        ]))
    ]))
])

# Compile and save the PyTeal program
with open("oracle.teal", "w") as f:
    compiled = compileTeal(program, Mode.Application)
    f.write(compiled)

# Get the latest confirmed block number
last_block = client.status()["lastRound"]

# Run the oracle
while True:
    try:
        result = client.pending_transactions
        for txn in result["transactions"]:
            if txn["lastRound"] <= last_block:
                continue

            last_block = txn["lastRound"]

            txn_id = txn["tx"]
            txn_info = client.pending_transaction_info(txn_id)

            if txn_info["type"] == "pay" and txn_info["from"] == researcher_address:
                try:
                    data = messaging.get_message(txn_id, oracle_address)
                    data = data.decode("utf-8")
                    txn_data = Bytes(data.encode("utf-8"))

                    txn_group = [
                        transaction.PaymentTxn(
                            contract_receiver,
                            contract_private_key,
                            contract_amount,
                            txn_info["receiver"],
                            last_block,
                            last_block + 1000,
                            txn_info["fee"],
                            flat_fee=True
                        ),
                        transaction.ApplicationCallTxn(
                            oracle_address,
                            client.suggested_params(),
                            int(contract_address),
                            [txn_data],
                            [],
                            last_block,
                            last_block + 1000,
                            txn_info["fee"],
                            flat_fee=True
                        )
                    ]

                    signed_group = [
                        txn_group[0].sign(contract_private_key),
                        txn_group[1].sign(oracle_private_key)
                    ]

                    client.send_transactions(signed_group)
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)
