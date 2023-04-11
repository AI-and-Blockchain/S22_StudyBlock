from pyteal import *

# Define the addresses of the sender and receiver
sender = Addr("SENDER_ADDRESS")
receiver = Addr("RECEIVER_ADDRESS")

# Define the local state variable to store the private key information
private_key = App.localPut(Bytes("privateKey"), Bytes(""))

# Condition for sending a message
send_message = And(
    Txn.sender() == sender,
    Txn.receiver() == receiver,
)

# Condition for sending the private key information
send_private_key = And(
    Txn.sender() == sender,
    Txn.receiver() == receiver,
    private_key[Txn.receiver()] == Bytes(""),
)

# Condition for retrieving the private key information
get_private_key = And(
    Txn.sender() == receiver,
    private_key[Txn.sender()] != Bytes(""),
)

# The main program logic
program = Cond(
    [send_message, App.localPut(Bytes("messages"), Txn.application_args[0])],
    [send_private_key, private_key[Txn.receiver()].store(Txn.application_args[0])],
    [get_private_key, Return(private_key[Txn.sender()])],
)

# Assemble the program and write to file
if __name__ == "__main__":
    with open("clinical_trial_messaging.teal", "w") as f:
        f.write(program.assemble())
