from models.nlp import Model
from messaging.ClinicalTrialMessaging import send_message
from oracle import runner, show_messages

def addTrial():
    print("Enter the new trial title to add: ")
    title = input()
    print("Enter the trial description: ")
    desc = input()
    print("Enter your address as a contact point: ")
    address = input()
    my_model.add_trial(title, description=desc, address=address)
    print("Trial stored")
    researchOutput()

def researchOutput():
    print("Would you like to [a]dd a trial, [c]heck your messages, or [e]xit?")
    line = input()
    if line == 'a' or line == 'A':
        addTrial()
    elif line == 'c' or line == "C":
        checkMessages(researcherAddress, 'r')
    elif line == 'e' or line == 'E':
        exit()

def search():
    print("Please enter any search terms: ")
    line = input()
    # load model and pass input into model
    # model returns list of relevant trials
    trials = my_model.search(line)
    print("Here are a list of current trials in that area:")

    index = 1
    for i in trials:
        print(index, i)
        index += 1

    print("Which trial would you like to access? (number)")
    line = int(input())
    print("Accessing", trials[line - 1])
    print("Would you like to [c]ontact the researcher or [s]end data?")
    line = input()
    if (line == 'c' or line == 'C'):
        # run the oracle to send messages
        print("Enter private key: ")
        patientKey = input()
        print("Enter receiver address: ")
        receiverAddress = input()
        print("Enter message: ")
        message = input()
        send_message(message=message, sender_pub=patientAddress, sender_priv=patientKey, receiver=receiverAddress)
    elif(line == 's' or line == 'S'):
        # execute atomic contract
        print("Enter private key: ")
        patientKey = input()
        print("Enter receiver address: ")
        receiverAddress = input()
        print("Enter data: ")
        data = input()
        message = f"DATA:{data}"
        send_message(message=message, sender_pub=patientAddress, sender_priv=patientKey, receiver=receiverAddress)
        runner(receiverAddress)
    patientOutput()

def checkMessages(address, _id):
    lst = show_messages(address)
    if len(lst) == 0:
        print("You have no messages")
    else:
        print("Here are your messages:")
        for s in lst:
            print(s[0], 'sent by', s[1])
    if _id == 'p':
        patientOutput()
    else:
        researchOutput()

def patientOutput():
    print("Would you like to [s]earch for trials, [c]heck you messages, or [e]xit?")
    line = input()
    if(line == 's' or line == 'S'):
        search()
    elif(line == 'c' or line =='C'):
        checkMessages(patientAddress, 'p')
    elif (line == 'e' or line == 'E'):
        exit()

my_model = Model()
# my_model.search('Chemotherapy trials for woman older than 30')
my_model.train_model()
passwords = ["CMU", "JHU", "RPI"]
print("Researcher (WIP) [R] or Patient [P]?")
line = input()
if line == "r" or line == "R":
    print("Input your identifier: ")
    line = input()
    if passwords.count(line) == 0:
        print("Invalid identifier, ending session")
        exit()
    print("Welcome", line)
    print("Enter your address: ")
    researcherAddress = input()
    researchOutput()
elif line == "p" or line == "P":
    print("Enter your address: ")
    patientAddress = input()
    patientOutput()
