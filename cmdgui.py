def researchOutput():
    print("Would you like to store, edit or delete a trial?")
    line = input()
    
    


def patientOutput():
    print("Please enter any search terms: ")
    line = input()
    # load model and pass input into model
    # model returns list of relevant trials
    trials = ["List", "of", "trials"]
    print("Here are a list of current trials in that area:\n", trials)
    print("Which trial would you like to access? (number)")
    line = int(input())
    print("Accessing", trials[line-1])


print("Researcher [R] or Patient [P]?")
line = input()
if line == "r" or line == "R":
    researchOutput()
elif line == "p" or line == "P":
    patientOutput()