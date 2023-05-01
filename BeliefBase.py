from sympy import *
import Sentence

# Implement BeliefBase class
class BeliefBase:
    def __init__(self):
        self.base = []
        self.baseIndex = 0
        self.symbolDict = {}
        self.base.append(Symbol("x"))
        self.base.append(Implies(Symbol("y"), Symbol("z")))
        self.base.append(Symbol("y"))
        self.base.append(Or(Symbol("x"), Symbol("a"), Symbol("b")))
        self.base.append(Not(Symbol("a")))
        self.base.append(Not(Symbol("b")))
    
    def check(self, sentence):
        clauses = FiniteSet()
        new = FiniteSet()
        for i in range(len(self.base)):
            clauseCNF = to_cnf(self.base[i])
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
        for c in range(len(clauseList)):
            if clauseList[c][0] == "~":
                clauseList[c] = Not(Symbol(clauseList[c][1:]))
            else:
                clauseList[c] = Symbol(clauseList[c])
        if len(clauseList) == 1:
            clause = clauseList[0]
        else:
            for i in range(len(clauseList)):
                if i == 0:
                    clause = Or(clauseList[i], clauseList[i+1])
                elif i == 1:
                    pass
                else:
                    clause = Or(clause, clauseList[i])
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
        clauses = FiniteSet()
        clauseTracker = {} # for tracking clauses back to their sentences
        new = FiniteSet()
        for i in range(len(self.base)):
            clauseCNF = to_cnf(self.base[i])
            clauseCNFSplitStr = self.separateClauseByAnd(clauseCNF)
            for subclause in clauseCNFSplitStr:
                clauseCNFSplit = self.makeClauseFromCNFStr(self.separateClauseByOr(subclause))
                clauseCNFSet = FiniteSet(clauseCNFSplit)
                clauses = Union(clauses, clauseCNFSet)
                clauseTracker[clauseCNFSplit] = [i]
        sentenceCNF = to_cnf(sentence.sentence)
        sentenceCNFSplitStr = self.separateClauseByAnd(sentenceCNF)
        for subclause in sentenceCNFSplitStr:
            sentenceCNFSplit = self.makeClauseFromCNFStr(self.separateClauseByOr(subclause))
            sentenceCNFSet = FiniteSet(sentenceCNFSplit)
            clauses = Union(clauses, sentenceCNFSet)
        while True:
            for i in clauses:
                isAlreadyChecked = False
                for j in clauses:
                    if i == j:
                        isAlreadyChecked = False
                        continue
                    if isAlreadyChecked:
                        continue
                    clause1IndexList = [] if i == sentence.sentence else clauseTracker[i]
                    clause2IndexList = [] if j == sentence.sentence else clauseTracker[j]
                    resolvedClause = self.resolve(i, j)
                    if resolvedClause == None:
                        removedClause = self.heuristic(i, j, sentence) # change this
                        removedIndexList = clauseTracker[removedClause]
                        removedIndexTraced = self.traceHeuristic(removedIndexList)
                        self.base.remove(self.base[removedIndexTraced])
                        return True
                    clauseTracker[resolvedClause] = [*set(clause1IndexList + clause2IndexList)]
                    resolvedClauseSet = FiniteSet(resolvedClause)
                    new = Union(new, resolvedClauseSet)
            if new.is_subset(clauses):
                return False
            clauses = Union(clauses, new)

    def uncontradict(self, sentence):
        isContradiction = True
        while isContradiction:
            isContradiction = self.remove(sentence)
    
    def traceHeuristic(self, indexList):
        max = 0
        removedIndex = 0
        for index in indexList:
            clause = str(to_cnf(self.base[index])).replace(" ","")
            if max < len(clause):
                max = len(clause)
                removedIndex = index
        return removedIndex


    def heuristic(self, clause1, clause2, sentence):
        if sentence.sentence == clause1:
            return clause2
        elif sentence.sentence == clause2:
            return clause1
        else:
            clause1Size = len(str(clause1).replace(" ",""))
            clause2Size = len(str(clause2).replace(" ",""))
            if clause1Size > clause2Size:
                return clause1
            else:
                return clause2
                              
    def add(self, sentence):
        for s in self.base:
            if sentence.sentence == s:
                print(str(sentence.sentence) + " already in belief base!") 
                return
        self.base.append(sentence.sentence)