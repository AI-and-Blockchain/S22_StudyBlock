from algosdk.v2client import indexer
from pyteal import *

# Account credentials
oracle_address = "ORACLE_ADDRESS"

# Atomic contract credentials
contract_address = "CONTRACT_ADDRESS"

# Algorand Indexer credentials
indexer_key = "YOUR_ALGOD_INDEXER_API_KEY"
indexer_address = "https://testnet-algorand.api.purestake.io/idx2"
indexer_client = indexer.IndexerClient(indexer_key, indexer_address)

# Define PyTeal program for the trigger
program = App.localGetEx(Int(0), Bytes("data"))

# Compile and save the PyTeal program
with open("trigger.teal", "w") as f:
    compiled = compileTeal(program, Mode.Application)
    f.write(compiled)

# Run the trigger
def run_trigger():
    try:
        result = indexer_client.search_applications(
            application_id=int(contract_address),
            include_all=True,
            limit=1,
            order="desc"
        )

        if len(result["applications"]) == 0:
            return

        app = result["applications"][0]
        global_state = app["params"]["global-state"]
        local_state = app["params"]["local-states"][oracle_address]

        last_block = None
        for state in global_state:
            if state["key"] == "oracleLastBlock":
                last_block = state["value"]["uint"]
                break

        if last_block is None:
            return

        for item in local_state:
            if item["key"] == "data" and item["value"]["uint"] > 0:
                value = item["value"]["bytes"]
                print(f"Triggered with value: {value.decode('utf-8')}")

    except Exception as e:
        print(e)

while True:
    run_trigger()
