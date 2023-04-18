from models.nlp import Model
from messaging.ClinicalTrialMessaging import send_message

def researchOutput():
    print("Input your identifier: ")
    line = input()
    if passwords.count(line) == 0:
        print("Invalid identifier, ending session")
        exit()
    print("Welcome", line)
    print("Would you like to add, edit or delete a trial?")
    line = input()
    if line == 's' or line == 'S':
        print("Enter the new trial title to add: ")
        title = input()
        print("Enter the trial description: ")
        desc = input()
        print("Enter your address as a contact point: ")
        address = input()
        my_model.add_trial(title, description=desc, address=address)
        print("Trial stored")
        exit()

def patientOutput():
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
    print("Would you like to contact the researcher?")
    line = input()
    if (line == 'y' or line == 'Y'):
        # run the oracle to send messages
        print("Enter your address: ")
        patientAddress = input()
        print("Enter private key: ")
        patientKey = input()
        print("Enter receiver address: ")
        receiverAddress = input()
        print("Enter message: ")
        message = input()
        send_message(message=message, sender_pub=patientAddress, sender_priv=patientKey, receiver=receiverAddress)

my_model = Model()
# my_model.search('Chemotherapy trials for woman older than 30')
my_model.train_model()
passwords = ["CMU", "JHU", "RPI"]
print("Researcher (WIP) [R] or Patient [P]?")
line = input()
if line == "r" or line == "R":
    researchOutput()
elif line == "p" or line == "P":
    patientOutput()
