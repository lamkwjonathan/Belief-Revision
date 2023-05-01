from sympy import *

# Implement BeliefBase class
class BeliefBase:
    """
    Class for belief base and its methods.
    """
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
        """
        Checks contradiction using the CNF-resolution method.
        """
        clauses = FiniteSet()
        new = FiniteSet()

        # Perform preliminary check whether sentence is already in the belief base
        for s in self.base:
            if s == sentence.sentence:
                print(str(sentence.sentence) + " already in belief base!")
                return False
            
        # Convert sentences in the belief base into CNF form and add them to the set of clauses
        for i in range(len(self.base)):
            clauseCNF = to_cnf(self.base[i])
            clauseCNFSplitStr = self.separateClauseByAnd(clauseCNF)
            for subclause in clauseCNFSplitStr:
                clauseCNFSplit = self.makeClauseFromCNFStr(self.separateClauseByOr(subclause))
                clauseCNFSet = FiniteSet(clauseCNFSplit)
                clauses = Union(clauses, clauseCNFSet)
        
        # Convert user input sentence into CNF form and add it to the set of clauses
        sentenceCNF = to_cnf(sentence.sentence)
        sentenceCNFSplitStr = self.separateClauseByAnd(sentenceCNF)
        for subclause in sentenceCNFSplitStr:
            sentenceCNFSplit = self.makeClauseFromCNFStr(self.separateClauseByOr(subclause))
            sentenceCNFSet = FiniteSet(sentenceCNFSplit)
            clauses = Union(clauses, sentenceCNFSet)

        # Resolve each pair of clauses together until there is an empty set (contradiction) or no more clauses left (no contradiction)
        while True:
            for i in clauses:
                isAlreadyChecked = False # Flag for skipping clauses that have already been resolved together
                for j in clauses:
                    if i == j:
                        isAlreadyChecked = False
                        continue
                    if isAlreadyChecked:
                        continue
                    resolvedClause = self.resolve(i, j)
                    if resolvedClause == None:
                        return True
                    resolvedClauseSet = FiniteSet(resolvedClause)
                    new = Union(new, resolvedClauseSet)
            if new.is_subset(clauses):
                return False
            clauses = Union(clauses, new)
    
    def resolve(self, clause1, clause2):
        """
        Resolves two CNF clauses together by removing complementary pairs.
        Returns a resolved clause in smypy form.
        """
        mergedClause = Or(clause1, clause2)
        mergedList = str(mergedClause).replace(" ", "").split("|")
        resolvedList = self.resolveSymbolsFromList(mergedList)
        resolvedClause = self.makeClauseFromCNFStr(resolvedList)
        return resolvedClause
    
    def makeClauseFromCNFStr(self, clauseList):
        """
        Takes in a list of symbols separated by commas and returns a CNF clause separated by |
        """
        clause = None
        # Convert symbols to sympy form
        for c in range(len(clauseList)):
            if clauseList[c][0] == "~":
                clauseList[c] = Not(Symbol(clauseList[c][1:]))
            else:
                clauseList[c] = Symbol(clauseList[c])
        
        # Create CNF form clause via Or() statements 
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
        """
        Takes in a list of symbols and returns a list of symbols with complementary symbols removed
        """
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
        """
        Takes in a sentence in CNF form and separates the clauses out by splitting along &.
        Returns a list of clauses.
        """
        clauseStr = str(clauseCNF)
        if clauseStr.find('&') == -1:
            return [clauseCNF]
        else:
            clauseList = clauseStr.replace(" ","").split("&")
            return clauseList
        
    def separateClauseByOr(self, clauseCNF):
        """
        Takes in a CNF clause and separates it by |.
        Returns a list of symbols.
        """
        clauseList = str(clauseCNF).replace(" ","").split("|")
        return clauseList

    def remove(self, sentence):
        """
        Removes contradiction using a variation of the CNF-resolution method.
        Every time an empty clause is obtained, one of the original offending clauses that caused it are removed.
        The removed clause is determined by the heuristic function.
        """
        clauses = FiniteSet()
        clauseTracker = {} # for tracking clauses back to their sentences
        new = FiniteSet()

        # Convert sentences in the belief base into CNF form and add them to the set of clauses
        for i in range(len(self.base)):
            clauseCNF = to_cnf(self.base[i])
            clauseCNFSplitStr = self.separateClauseByAnd(clauseCNF)
            for subclause in clauseCNFSplitStr:
                clauseCNFSplit = self.makeClauseFromCNFStr(self.separateClauseByOr(subclause))
                clauseCNFSet = FiniteSet(clauseCNFSplit)
                clauses = Union(clauses, clauseCNFSet)
                clauseTracker[clauseCNFSplit] = [i] # stores location of sentence in the belief base in a dictionary
        
        # Convert user input sentence into CNF form and add them to the set of clauses
        sentenceCNF = to_cnf(sentence.sentence)
        sentenceCNFSplitStr = self.separateClauseByAnd(sentenceCNF)
        for subclause in sentenceCNFSplitStr:
            sentenceCNFSplit = self.makeClauseFromCNFStr(self.separateClauseByOr(subclause))
            sentenceCNFSet = FiniteSet(sentenceCNFSplit)
            clauses = Union(clauses, sentenceCNFSet)
            clauseTracker[sentenceCNFSplit] = [-1] # stores value of -1 as a flag in the dictionary
        
        # Perform resolution for each pair of clauses. 
        # Every time a new clause is created and added to the clauses set, a corresponding key-value pair is added to the clauseTracker
        # to store the indexes of the sentences that formed the new clause.
        while True:
            for i in clauses:
                isAlreadyChecked = False
                for j in clauses:
                    if i == j:
                        isAlreadyChecked = False
                        continue
                    if isAlreadyChecked:
                        continue
                    clause1IndexList = clauseTracker[i]
                    clause2IndexList = clauseTracker[j]
                    resolvedClause = self.resolve(i, j)
                    if resolvedClause == None:
                        removedIndexList = [*set(clause1IndexList + clause2IndexList)]
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
        """
        Loop function to keep running the remove method until no more contradictions exist in the belief base.
        """
        isContradiction = True
        while isContradiction:
            isContradiction = self.remove(sentence)
    
    def traceHeuristic(self, indexList):
        """
        Method to choose which parent sentence of the offending clauses to remove.
        """
        min = 100000
        removedIndex = 0
        for index in indexList:
            if index == -1: # skips over the user input sentence
                continue
            clause = str(to_cnf(self.base[index])).replace(" ","")
            if min > len(clause):
                min = len(clause)
                removedIndex = index
        return removedIndex

    def add(self, sentence):
        """
        Adds a sentence to the belief base.
        Does not add repeated sentences.
        """
        for s in self.base:
            if sentence.sentence == s: 
                return
        self.base.append(sentence.sentence)