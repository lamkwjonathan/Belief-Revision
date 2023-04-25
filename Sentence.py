from sympy import *

# Implement Sentence Class that strips a string input into its symbols and commands
class Sentence:
    def __init__(self, rawText):
        self.rawText = rawText
        self.symbols = []
        self.sentence = None
        self.makeNewSentence(self.rawText)

    '''
    def makeNewSentence(self, rawText):
        text = rawText.replace(" ", "")
        for c in range(len(text)):
            if text[c] == "(":
                for z in range(len(text)-1, -1, -1):
                    if text[z] == ")":
                        return self.makeNewSentence(text[c:z]) # And(x, y) (x, y, &)
        textList = text.split(",")
        if len(textList) < 2:
            return self.makeUnitSentence(textList[0], textList[1])
        elif len(textList) < 3:
            return self.makeUnitSentence(textList[0], textList[1], textList[2])
        else:
            raise Exception("Invalid sentence structure: too many arguments!")
    '''

    def makeNewSentence(self, rawText):
        # ((x, y, |), (z, ~), &)
        text = rawText.replace(" ", "")
        # ((x,y,|),(z,~),&)
        text = self.stripBracket(text)
        # (x,y,|),(z,~),&
        argsList = self.splitArgs(text)
        # [(x,y,|), (z,~), &]
        
        if len(argsList) >= 3:
            raise Exception("Invalid sentence structure: too many arguments!")

        operand = argsList[-1]
        if operand == "~":
            return self.makeUnitSentence(argsList[0], argsList[1])
        else:
            return self.makeUnitSentence(argsList[0], argsList[1], argsList[2])
        
    def stripBracket(self, text):
        for c in range(len(text)):
            if text[c] == "(":
                for z in range(len(text)-1, -1, -1):
                    if text[z] == ")":
                        return text[c:z]
                    
    def splitArgs(self, text):
        argsList = []

        startIndex = 0
        endIndex = 0
        openBracketCount = 0
        closeBracketCount = 0
        argStartFlag = 1

        for i in range(len(text)):
            if argStartFlag == 1:
                if text[i] != "(":
                    startIndex = i
                    j = i
                    while text[j] != ",":
                        j += 1
                    endIndex = j
                    argsList.append(text[startIndex, endIndex])
                    startIndex = 0
                    endIndex = 0
                    i += 1
                else:
                    argStartFlag = 0
            
            if text[i] == "(":
                openBracketCount += 1
                startIndex = i
            elif text[i] == ")":
                closeBracketCount += 1
                endIndex = i+1
            if openBracketCount == closeBracketCount:
                argsList.append(text[startIndex, endIndex])
                openBracketCount = 0
                closeBracketCount = 0
                i += 1
                argStartFlag = 1
        
        return argsList

    def makeUnitSentence(self, *args): 
        try:
            operand = args[-1]
            args1 = args[0]
            if len(args) > 2:
                args2 = args[1]
            
                if args1[0] != "(" and args2[0] != "(":
                    if operand == "&":
                        return And(Symbol(args[0]), Symbol(args[1]))
                    elif operand == "|":
                        return Or(Symbol(args[0]), Symbol(args[1]))
                    elif operand == ">>":
                        return Implies(Symbol(args[0]), Symbol(args[1]))    
                elif args1[0] == "(" and args2[0] != "(":
                    pass

        except:
            print("Invalid sentence structure!")

    def isOperand(self, item):
        if item == "&":
            return True
        elif item == "|":
            return True
        elif item == ">>":
            return True
        else:
            return False
        
    
