def researchOutput():
    print("Input your identifier: ")
    line = input()
    if passwords.count(line) == 0:
        print("Invalid identifier, ending session")
        exit()
    print("Welcome", line)
    print("Would you like to store, edit or delete a trial?")
    line = input()
    if line == 's' or line == 'S':
        print("Enter the new trial to add: ")
        line = input()
        # add given trial to the database or asset - depending on how we are storing them
        print("Enter the trial description: ")
        line = input()
        # same as above
        print("Trial stored")
        exit()
    elif line == 'e' or 'E':
        print()

def patientOutput():
    print("Please enter any search terms: ")
    line = input()
    # load model and pass input into model
    # model returns list of relevant trials
    trials = ["List", "of", "trials"]
    print("Here are a list of current trials in that area:")
    
    index = 1
    for i in trials:
        print(index, i)
        index += 1
    
    print("Which trial would you like to access? (number)")
    line = int(input())
    print("Accessing", trials[line-1])

passwords = ["CMU", "JHU", "RPI"]
print("Researcher [R] or Patient [P]?")
line = input()
if line == "r" or line == "R":
    researchOutput()
elif line == "p" or line == "P":
    patientOutput()