from pyteal import *

message = App.localPut(Bytes("message"), Bytes(""))

update_message = And(
    Txn.sender() == App.creator(),
    Txn.application_args[0] == Bytes("updateMessage"),
)

program = Cond(
    [update_message, message.store(Txn.application_args[1])],
)

if __name__ == "__main__":
    with open("transact_message.teal", "w") as f:
        f.write(program.assemble())
