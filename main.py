from sympy import *
from BeliefBase import BeliefBase
from Command import Command
    
def parse(userInput, command, beliefBase):
    """
    Parses user input and returns one of 3 appropriate commands.
    """
    userInputList = userInput.replace(" ","").split(":")
    if userInputList[0] == 'end':
        return command.end()
    elif userInputList[0] == 'list':
        return command.list(beliefBase)
    elif userInputList[0] == 'check':
        return command.check(userInputList[1], beliefBase)
    elif userInputList[0] == 'add': #add will check, remove contradiction, then add
        return command.add(userInputList[1], beliefBase)
    else:
        return command.invalid()

if __name__ == "__main__":
    notProgramEnded = True
    
    bb = BeliefBase()
    command = Command()

    print("Belief Revision Agent")
    print("---Operands---")
    print("and      :    &")
    print("or       :    |")
    print("not      :    ~")
    print("implies  :    >")
    print("---Format---")
    print("(symbol_1, symbol_2, operand)")
    print("Only 2 symbols are allowed in each set of brackets.")
    print("Multiple and/or chains can be created by nesting brackets:")
    print("((x, y, |), z, |)")
    print("Equivalence can be coded by using two implications:")
    print("((a,b,>), (b,a,>), &)")
    print("---Commands---")
    print("list                                    -- for listing all sentences in the belief base")
    print("check: (symbol_1, symbol_2, operand)    -- for checking for contradictions (does not alter the belief base)")
    print("add: (symbol_1, symbol_2, operand)      -- for adding new sentences to the belief base (does contradiction check too)")
    print("end                                     -- for ending the program")
    print("---Examples---")
    print("add: x")
    print("add : (y,~)")
    print("add  :  ( (x,y,>), z, | )")
    print("--------------")
    print("")

    while notProgramEnded:
        userInput = input()
        notProgramEnded = parse(userInput, command, bb)
    print("Program ended")

    

    