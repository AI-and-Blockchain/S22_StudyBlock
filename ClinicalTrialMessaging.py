from pyteal import *

messages = App.localPut(Bytes("messages"), App.localGetEx(Int(0), Bytes("sender")))

send_message = And(
    Txn.receiver() != Txn.sender(),
)

get_message = messages[App.localGetEx(Int(0), Bytes("sender"))][Txn.sender()].value()

program = Cond(
    [send_message, messages[App.localGetEx(Int(0), Bytes("sender"))][Txn.receiver()].store(Txn.application_args[0])],
    [Txn.application_args[0] == Bytes("getMessage"), Return(get_message)],
)

if __name__ == "__main__":
    with open("clinical_trial_messaging.teal", "w") as f:
        f.write(program.assemble())
