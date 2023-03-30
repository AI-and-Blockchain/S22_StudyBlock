from pyteal import *

client = Addr("CLIENT_ADDRESS")
private_key = Bytes("0x")
backend_users = App.localPut(Bytes("backendUsers"), Addr("BACKEND_USERS"))

private_key_sent = And(
    Txn.sender() == client,
    Txn.receiver() != Global.current_application_address(),
)

add_backend_user = And(
    Txn.sender() == client,
    backend_users[Txn.application_args[0]] == Int(0),
)
remove_backend_user = And(
    Txn.sender() == client,
    backend_users[Txn.application_args[0]] == Int(1),
)

send_data = And(
    backend_users[Txn.sender()] == Int(1),
    private_key != Bytes("0x"),
)

program = Cond(
    [private_key_sent, private_key.store(Txn.application_args[0])],
    [add_backend_user, backend_users[Txn.application_args[0]].store(Int(1))],
    [remove_backend_user, backend_users[Txn.application_args[0]].store(Int(0))],
    [send_data, App.localPut(Bytes("data"), Txn.application_args[0])],
)

if __name__ == "__main__":
    with open("clinical_trial.teal", "w") as f:
        f.write(program.assemble())
