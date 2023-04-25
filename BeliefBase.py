from sympy import *
import Sentence

# Implement BeliefBase class
class BeliefBase:
    def __init__(self, maxMem):
        self.base = [None]*maxMem #decide on data structure for storage
        self.baseIndex = 0
        self.symbolDict = {}
    
    def check(self):
        return True
    
    def resolve(self, sentence):
        return self.base
    
    def add(self, sentence):
        return self.base
