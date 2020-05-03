class mapper():
    def __init__(self, reference, sequence, trie, patch=-1):
        self.reference = reference
        self.sequence = sequence
        self.trie = trie
        self.patch = patch
        self.matching = dict()
        self.add_reference()
        self.map_sequence(self.patch)

    def add_reference(self):
        for sequenceName in self.reference.kmers:
            for kmer in self.reference.kmers[sequenceName]:
                self.trie.add_suffix(kmer[0], sequenceName, kmer[1])

    def map_sequence(self, patch=-1):
        if patch == -1:
            for sequenceName in self.sequence.kmers:
                for kmer in self.sequence.kmers[sequenceName]:
                    refMatched = self.trie.find_suffix(kmer[0])
                    if refMatched != -1:
                        self.match(sequenceName, kmer[1], refMatched)
        else:
            self.sequence.dump(self.sequence.seq.filePrefix)
            if self.sequence.load(self.sequence.seq.filePrefix, self.patch):
                return
            self.map_sequence()
            self.map_sequence(self.patch)

    def match(self, sequenceName, kPos, refMatched):
        if sequenceName not in self.matching:
            self.matching[sequenceName] = dict()
        matchInst = self.matching[sequenceName]
        for refInst in refMatched:
            if refInst[0] not in matchInst:
                matchInst[refInst[0]] = []
            matched = [[kPos, self.reference.k], refInst[1]]
            matchInst[refInst[0]].append(matched)

    def filter_matching(self, minKmer, minQuotient):
        emptyRef = []
        k = self.reference.k
        for sequenceName in self.matching:
            for refName in self.matching[sequenceName]:
                matchInst = self.matching[sequenceName][refName]
                concatenated = False
                start = 0
                while not concatenated:
                    concList = []
                    comp1 = matchInst[start]
                    for i in range(start+1, len(matchInst)):
                        comp2 = matchInst[i]
                        if comp2[0][0]-comp1[0][0] == comp2[1]-comp1[1]:
                            if comp2[0][0] >= comp1[0][0]+comp1[0][1]:
                                concLen = comp2[0][0]+comp2[0][1]-comp1[0][0]
                                comp1[0][1] = concLen
                                concList.append(comp2)
                    matchInst = [x for x in matchInst if x not in concList]
                    quotient = ((len(concList)+1) * k / comp1[0][1])*100
                    if len(concList)+1 < minKmer or quotient < minQuotient:
                        matchInst.pop(start)
                    self.matching[sequenceName][refName] = matchInst
                    if matchInst == []:
                        emptyRef.append([sequenceName, refName])
                    start += 1
                    if start >= len(matchInst):
                        if matchInst != []:
                            if matchInst[0][0][1] < minKmer*k:
                                matchInst.pop(0)
                                emptyRef.append([sequenceName, refName])
                        concatenated = True
        tmp = self.matching
        for refName in emptyRef:
            tmp[refName[0]].pop(refName[1])
        tmp = {x: y for x, y in zip(tmp.keys(), tmp.values()) if y != dict()}
        self.matching = tmp
        del tmp
