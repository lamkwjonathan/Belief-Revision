from sympy import *

# Implement Sentence Class that strips a string input into its symbols and commands
class Sentence:
    """
    Class for transforming and storing user input into sympy logic form.
    """
    def __init__(self, rawText):
        self.rawText = rawText
        self.symbols = []
        self.sentence = self.makeNewSentence(self.rawText)

    def makeNewSentence(self, rawText):
        """
        Takes in a string and transforms it into sympy form.
        """
        text = rawText.replace(" ", "")
        if text[0] != "(": # Single variable entered
            return Symbol(text)
        #print(text)
        text = self.stripBracket(text)
        #print(text)
        argsList = self.splitArgs(text)
        #print(argsList)
        
        if len(argsList) > 3:
            raise Exception("Invalid sentence structure: too many arguments!")

        operand = argsList[-1]
        if operand == "~":
            return self.makeUnitSentence(argsList[0], argsList[1])
        else:
            return self.makeUnitSentence(argsList[0], argsList[1], argsList[2])
        
    def stripBracket(self, text):
        """
        Removes one layer of brackets from a user input string
        """
        for c in range(len(text)):
            if text[c] == "(":
                for z in range(len(text)-1, -1, -1):
                    if text[z] == ")":
                        return text[c+1:z]
                    
    def splitArgs(self, text):
        """
        Splits a string along commas, taking into account brackets that demarcate clauses that have to stay together.
        """
        argsList = []

        startIndex = 0
        endIndex = 0
        openBracketCount = 0
        closeBracketCount = 0
        argStartFlag = 1

        for i in range(len(text)):
            if argStartFlag == 1:
                startIndex = i
                if text[i] == ",":
                    pass
                elif text[i] != "(":
                    j = i
                    while j < len(text) and text[j] != ",":
                        j += 1
                    endIndex = j
                    argsList.append(text[startIndex:endIndex])
                    startIndex = 0
                    endIndex = 0
                else:
                    argStartFlag = 0
            
            if text[i] == "(":
                openBracketCount += 1
            elif text[i] == ")":
                closeBracketCount += 1
                endIndex = i+1
            if openBracketCount == closeBracketCount and openBracketCount != 0:
                argsList.append(text[startIndex:endIndex])
                openBracketCount = 0
                closeBracketCount = 0
                i += 1
                argStartFlag = 1
        
        return argsList

    def makeUnitSentence(self, *args): 
        """
        Recursive function that applies sympy logic functions to the user input in the correct order to create a sympy logical expression.
        """
        try:
            operand = args[-1]
            args1 = args[0]

            if args1[0] == "(":
                    args1 = self.stripBracket(args1)
                    args1List = self.splitArgs(args1)
                    if args1[-1] != "~":
                        args1 = self.makeUnitSentence(args1List[0], args1List[1], args1List[-1])
                    else:
                        args1 = self.makeUnitSentence(args1List[0], args1List[-1])

            if len(args) > 2:
                args2 = args[1]
            
                if args2[0] == "(":
                    args2 = self.stripBracket(args2)
                    args2List = self.splitArgs(args2)
                    if args2[-1] != "~":
                        args2 = self.makeUnitSentence(args2List[0], args2List[1], args2List[-1])
                    else:
                        args2 = self.makeUnitSentence(args2List[0], args2List[-1])
                if type(args1) != Or and type(args1) != And and type(args1) != Not and type(args1) != Implies and type(args1) != Symbol:
                    args1 = Symbol(args1)
                if type(args2) != Or and type(args2) != And and type(args2) != Not and type(args2) != Implies and type(args2) != Symbol:
                    args2 = Symbol(args2)
                if operand == "&":
                    return And(args1, args2)
                elif operand == "|":
                    return Or(args1, args2)
                elif operand == ">":
                    return Implies(args1, args2)    
                elif operand == "=":
                    return Equivalent(args1, args2)
            
            if operand == "~":
                return Not(args1)

        except:
            print("Invalid sentence structure!")

    
