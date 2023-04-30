from sympy import *
import Sentence

# Implement BeliefBase class
class BeliefBase:
    def __init__(self):
        self.base = []
        self.baseIndex = 0
        self.symbolDict = {}
        self.base.append(Symbol("x"))
        self.base.append(And(Symbol("y"), Symbol("z")))
        self.base.append(Not(Symbol("a")))
    
    def check(self, sentence):
        clauses = FiniteSet()
        new = FiniteSet()
        for clause in self.base:
            clauseCNF = to_cnf(clause)
            clauseCNFSplitStr = self.separateClauseByAnd(clauseCNF)
            for subclause in clauseCNFSplitStr:
                clauseCNFSplit = self.makeClauseFromCNFStr(self.separateClauseByOr(subclause))
                clauseCNFSet = FiniteSet(clauseCNFSplit)
                clauses = Union(clauses, clauseCNFSet)
        sentenceCNF = to_cnf(sentence.sentence)
        sentenceCNFSplitStr = self.separateClauseByAnd(sentenceCNF)
        for subclause in sentenceCNFSplitStr:
            sentenceCNFSplit = self.makeClauseFromCNFStr(self.separateClauseByOr(subclause))
            sentenceCNFSet = FiniteSet(sentenceCNFSplit)
            clauses = Union(clauses, sentenceCNFSet)
        while True:
            for i in clauses:
                for j in clauses:
                    #print("i", i)
                    #print("j", j)
                    resolvedClause = self.resolve(i, j)
                    if resolvedClause == None:
                        return True
                    resolvedClauseSet = FiniteSet(resolvedClause)
                    new = Union(new, resolvedClauseSet)
            if new.is_subset(clauses):
                return False
            clauses = Union(clauses, new)
    
    def resolve(self, clause1, clause2):
        mergedClause = Or(clause1, clause2)
        mergedList = str(mergedClause).replace(" ", "").split("|")
        resolvedList = self.resolveSymbolsFromList(mergedList)
        resolvedClause = self.makeClauseFromCNFStr(resolvedList)
        return resolvedClause
    
    def makeClauseFromCNFStr(self, clauseList):
        clause = None
        if len(clauseList) == 1:
            clause = Symbol(clauseList[0])
        else:
            for i in range(len(clauseList)):
                if i == 0:
                    clause = Or(Symbol(clauseList[i]), Symbol(clauseList[i+1]))
                elif i == 1:
                    pass
                else:
                    clause = Or(clause, Symbol(clauseList[i]))
                
        return clause

    def resolveSymbolsFromList(self, symList):
        resolvedList = []
        for s in symList:
            contradict = False
            if s[0] == '~':
                for sym in resolvedList:
                    if sym == s[1:]:
                        resolvedList.remove(sym)
                        contradict = True
            else:
                for sym in resolvedList:
                    if sym[0] == "~" and sym[1:] == s:
                        resolvedList.remove(sym)
                        contradict = True
            if contradict == False:
                resolvedList.append(s)
        return resolvedList
    
    def separateClauseByAnd(self, clauseCNF):
        clauseStr = str(clauseCNF)
        if clauseStr.find('&') == -1:
            return [clauseCNF]
        else:
            clauseList = clauseStr.replace(" ","").split("&")
            return clauseList
        
    def separateClauseByOr(self, clauseCNF):
        clauseList = str(clauseCNF).replace(" ","").split("|")
        return clauseList


    def remove(self, sentence):
        return self.base
    
    def add(self, sentence):
        return self.base
