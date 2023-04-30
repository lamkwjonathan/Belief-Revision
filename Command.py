from Sentence import Sentence

# Implement Command class
class Command:
    def __init__(self):
        pass

    def end(self, notProgramEnded):
        notProgramEnded = False

    def check(self, rawText, beliefBase):
        sentence = Sentence(rawText)
        print("sentence:", sentence.sentence)
        isContradiction = beliefBase.check(sentence)
        if isContradiction:
            print(str(sentence.sentence) + " contradicts with belief base!")
        else:
            print(str(sentence.sentence) + " doesn't contradict with belief base!")

    def add(self, rawText, beliefBase):
        '''
        check: cnf -- smash statements together theres nothing left, there is a empty set (contradiction). If pass check then skip resolution step.
        resolve: choose uwhich contradictions to kick using principles (priority based on time)
        add: add actual statement & decide which statements to float up (need to sort)
        
        ##Question: how do we surface all the possible resolutions to choose the best one based on our priority?
        '''
        sentence = Sentence(rawText)
        isContradiction = beliefBase.check(sentence)
        if isContradiction:
            beliefBase.resolve(sentence)
        beliefBase.add(sentence)
        
