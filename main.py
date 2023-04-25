from sympy import *
import BeliefBase
import Command

MAXMEM = 1000
    
def parse(self, userInput, command, beliefBase, notProgramEnded):
    userInputList = userInput.split(": ")
    if userInputList[0] == 'end':
        return command.end(notProgramEnded)
    elif userInput[0] == 'check':
        return command.check(userInputList[1], beliefBase)
    elif userInputList[0] == 'add': #add will check, remove contradiction, then add
        return command.add(userInputList[1], beliefBase)

if __name__ == "__main__":
    notProgramEnded = True
    
    bb = BeliefBase(MAXMEM)
    command = Command()

    print("Belief Revision Agent")
    print("---Commands---")
    print("check: (y, (a, b, |), |) -- for checking for contradictions (does not add to the belif base)")
    print("add: ((x, y, &), ~) -- for adding new sentences to the belief base")
    print("end -- for ending the program")

    while notProgramEnded:
        userInput = input()
        parse(userInput, command, notProgramEnded, bb)
    
    print("Program ended")

    

    