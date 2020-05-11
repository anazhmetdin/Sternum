from trie import Trie
from sufxArr import SA


class mapper():
    def __init__(self, refKmer, seqKmer, spine, batchSize=-1):
        """
 Takes reference and sequence as kmer_maker() objects and spine() object\
 ,then, it starts adding the reference to the spine kmer by kmer.\
 Then, starts mapping the sequence based on the batchSize, if batchSize != -1\
 it will automatically dump data to the disk and loads batch by batch
        """
        self.refKmer = refKmer
        self.seqKmer = seqKmer
        self.spine = spine
        self.batchSize = batchSize
        self.matching = dict()
        self.add_reference()
        self.map_sequence(self.batchSize)

    def add_reference(self):
        """
 It adds the reference to the spine kmer by kmer
        """
        current_pos = 0
        for readID in self.refKmer.kmers:
            for kmer in self.refKmer.kmers[readID]:
                if isinstance(self.spine, Trie):
                    self.spine.add_suffix(kmer[0], readID, kmer[1])
                elif isinstance(self.spine, SA):
                    actual_pos = current_pos + kmer[1]
                    self.spine.add_suffix(kmer[0], actual_pos)
                    temp = actual_pos
            current_pos += len(self.refKmer.seq.seq[readID])
        if isinstance(self.spine, SA):
            self.spine.add_suffix(kmer[0], temp, True)

    def map_sequence(self, batchSize=-1):
        """
 It maps the sequence based on the batchSize, if batchSize != -1\
 it will automatically dump data to the disk and loads batch by batch
        """
        if batchSize == -1:
            for readID in self.seqKmer.kmers:
                for kmer in self.seqKmer.kmers[readID]:
                    refMatched = self.spine.find_suffix(kmer[0])
                    if refMatched != -1:
                        self.match(readID, kmer[1], refMatched)
        else:
            self.seqKmer.dump(self.seqKmer.filePrefix)
            if self.seqKmer.load(self.seqKmer.filePrefix, self.batchSize):
                return
            self.map_sequence()
            self.map_sequence(self.batchSize)

    def match(self, readID, kPos, refMatched):
        """
 It taks readID = str(), kPos = int() kmer position,and refMatched = listt()\
 following this pattern:
 [[readID, kmer-pos], [readID, kmer-pos], ..., [readID, kmer-pos]]
 Them, it fills "matching", which is a dictionary following this pattern:
 {readID: {refID: [[[kPos, k-size], refPos], [[kPos, k-size], refPos]]}
 readID: {refID: [[[kPos, k-size], refPos]], refID: [[[kPos, k-size], refPos]]}
  .
  .
  .
  readID: {refID: [[[kPos, k-size], refPos], [[kPos, k-size], refPos]]}}
        """
        if readID not in self.matching:
            self.matching[readID] = dict()
        matchInst = self.matching[readID]
        for refInst in refMatched:
            if refInst[0] not in matchInst:
                matchInst[refInst[0]] = []
            matched = [[kPos, self.refKmer.k], refInst[1]]
            matchInst[refInst[0]].append(matched)

    def filter_matching(self, minKmer=10, minQuotient=70):
        """
 It taks minKmer = int() minimum number of kmers matching the refernce to keep\
 the read in "matching", and minQuotient = int() from 0 to 100 minimum\
 percentage of read kmers covering the refernce from start to end of the\
 covered aread only
        """
        emptyRef = []  # to store referenceID which no longer has matches
        k = self.refKmer.k
        for readID in self.matching:  # {refID: [[[kPos, k-size]], refID:....
            for refID in self.matching[readID]:
                matchInst = self.matching[readID][refID]  # [[[kPos, k], rpos]]
                concatenated = False  # to detect when "matchInst" is empty
                start = 0
                while not concatenated:
                    concList, kmerCount = concatenate(matchInst, start)
                    matchInst = [x for x in matchInst if x not in concList]
                    quotient = (kmerCount * k / matchInst[start][0][1])*100
                    if kmerCount < minKmer or quotient < minQuotient:
                        matchInst.pop(start)
                        if len(matchInst) == 1:
                            matchInst = []
                    if matchInst == []:
                        emptyRef.append([readID, refID])
                    self.matching[readID][refID] = matchInst
                    if start >= len(matchInst) - 1:
                        concatenated = True
        tmp = self.matching
        for refID in emptyRef:  # remove reference matches not meeting quality
            tmp[refID[0]].pop(refID[1])
        # remove reads having no qualified matches
        tmp = {x: y for x, y in zip(tmp.keys(), tmp.values()) if y != dict()}
        self.matching = tmp
        del tmp


def concatenate(matchInst, start):
    concList = []
    comp1 = matchInst[start]
    for i in range(start+1, len(matchInst)):
        comp2 = matchInst[i]
        # if difference between kPos and Rpos is the same
        if comp2[0][0]-comp1[0][0] == comp2[1]-comp1[1]:
            # if second kmer starts after the fist kmer
            # to avoid overlapping
            if comp2[0][0] >= comp1[0][0]+comp1[0][1]:
                concLen = comp2[0][0]+comp2[0][1]-comp1[0][0]
                comp1[0][1] = concLen  # from kmer1's start to kmer2's end
                concList.append(comp2)  # to be deleted later
    return concList, (len(concList)+1)
