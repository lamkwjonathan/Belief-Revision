from Sentence import Sentence

# Implement Command class
class Command:
    """
    Class for holding the command functions the user is allowed to call.
    """
    def __init__(self):
        pass

    def end(self):
        """
        Ends the program.
        """
        return False

    def list(self, beliefBase):
        print("")
        print("Current Belief Base:")
        for s in range(len(beliefBase.base)):
            print(str(s+1) + ".  " + str(beliefBase.base[s]))
        print("")
        return True

    def check(self, rawText, beliefBase):
        """
        Checks if the sentence given by the user is in contradiction with the current belief base.
        Does not change the current belief base.
        """
        sentence = Sentence(rawText)
        print("")
        print("Check sentence:", sentence.sentence)
        print("Checking... might take a few moments...")
        isContradiction = beliefBase.check(sentence)
        if isContradiction:
            print(str(sentence.sentence) + " contradicts with belief base!")
        else:
            print(str(sentence.sentence) + " doesn't contradict with belief base!")
        print("")
        return True

    def add(self, rawText, beliefBase):
        """
        Checks if the sentence given by the user is in contradiction with the current belief base.
        If so, remove contradicting sentences, then adds new sentence to the belief base. 
        """
        sentence = Sentence(rawText)
        print("")
        print("Add sentence:", sentence.sentence)
        print("Checking... might take a few moments...")
        isContradiction = beliefBase.check(sentence)
        if isContradiction:
            print(str(sentence.sentence) + " contradicts with belief base!")
            print("Old Belief Base:")
            print(beliefBase.base)
            print("Resolving... might take a few minutes...")
            beliefBase.uncontradict(sentence)
        else:
            print(str(sentence.sentence) + " doesn't contradict with belief base!")
        beliefBase.add(sentence)
        print("New Belief Base:")
        print(beliefBase.base)
        print("")
        return True

    def invalid(self):
        print("")
        print("Invalid command!")
        print("")
        return True
        
