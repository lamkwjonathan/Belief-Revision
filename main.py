from sympy import *
from BeliefBase import BeliefBase
from Command import Command

MAXMEM = 1000
    
def parse(userInput, command, beliefBase, notProgramEnded):
    userInputList = userInput.split(": ")
    print(userInputList)
    if userInputList[0] == 'end':
        return command.end(notProgramEnded)
    elif userInputList[0] == 'check':
        return command.check(userInputList[1], beliefBase)
    elif userInputList[0] == 'add': #add will check, remove contradiction, then add
        return command.add(userInputList[1], beliefBase)

if __name__ == "__main__":
    notProgramEnded = True
    
    bb = BeliefBase(MAXMEM)
    command = Command()

    print("Belief Revision Agent")
    print("---Operands---")
    print("and      :    &")
    print("or       :    |")
    print("not      :    ~")
    print("implies  :    >")
    print("---Format---")
    print("(symbol_1, symbol_2, operand)")
    print("Only 2 symbols are allowed in each set of brackets. Multiple and/or chains can be created by nesting brackets:")
    print("((x, y, |), z, |)")
    print("---Commands---")
    print("check    :    (y, (a, b, |), |) -- for checking for contradictions (does not add to the belif base)")
    print("add      :    ((x, y, &), ~) -- for adding new sentences to the belief base")
    print("end      :    for ending the program")


    while notProgramEnded:
        userInput = input()
        parse(userInput, command, notProgramEnded, bb)
    
    print("Program ended")

    

    