from trie import Trie
from sufxArr import SA
from BWT import BWT


class mapper():
    """main class of sternum and responsible for match reference to kmers.

    Attributes
    ----------
    matching : dict
{readID: {refID: [[[kPos, k-size], refPos], [[kPos, k-size], refPos]]}
 readID: {refID: [[[kPos, k-size], refPos]], refID: [[[kPos, k-size], refPos]]}

    Parameters
    ----------
    reference : kmer_maker or decoder
        if matching using Trie or sufxArr, should be kmer_maker.
        if matching using BWT, should be decoder
    seqKmer : kmer_maker
        kmers of the sequence to be matched.
    spine : Trie, or sufxArr, or BWT
        where reference will be stored for matching.
    batchSize : int
        number of files to be matched per iteration, if -1 no batches are used.

    """

    def __init__(self, reference, seqKmer, spine, batchSize=-1):
        """adds the reference to the spine then mapa the sequence\
        based on batchSize.

        Parameters
        ----------
        reference : kmer_maker or decoder
            if matching using Trie or sufxArr, should be kmer_maker.
            if matching using BWT, should be decoder
        seqKmer : kmer_maker
            kmers of the sequence to be matched.
        spine : Trie, or sufxArr, or BWT
            where reference will be stored for matching.
        batchSize : int
            number of files to be matched per iteration,
            if -1 no batches are used.

        """
        self.reference = reference
        self.seqKmer = seqKmer
        self.spine = spine
        self.batchSize = batchSize
        self.matching = dict()
        self.add_reference()
        self.map_sequence(self.batchSize)

    def add_reference(self):
        """
        adds the reference to the spine
        """
        if isinstance(self.spine, BWT):
            refV = list(self.reference.seq.values())
            reference_conc = "".join([x for x in refV])+'$'
            for i in range(len(reference_conc)):
                self.spine.add_suffix(reference_conc[i:], i)
            self.spine.add_suffix(reference_conc[i:], i, reference_conc, True)
            del reference_conc
        else:
            current_pos = 0
            for readID in self.reference.kmers:
                for kmer in self.reference.kmers[readID]:
                    if isinstance(self.spine, Trie):
                        self.spine.add_suffix(kmer[0], readID, kmer[1])
                    elif isinstance(self.spine, SA):
                        actual_pos = current_pos + kmer[1]
                        self.spine.add_suffix(kmer[0], actual_pos)
                        temp = actual_pos
                current_pos += len(self.reference.seq.seq[readID])
            if isinstance(self.spine, SA):
                self.spine.add_suffix(kmer[0], temp, True)

    def map_sequence(self, batchSize=-1):
        """maps the sequence based on the batchSize.

        Parameters
        ----------
        batchSize : int
            number of files to be matched per iteration,
            if -1 no batches are used.

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
        """append match instance to matching dictionary.

        Parameters
        ----------
        readID : str
            readID of the sequence matched to reference.
        kPos : int
            kmer position in sequence.
        refMatched : list
            [[readID, matchPos], [readID, matchPos], ..., [readID, matchPos]]
        """
        if readID not in self.matching:
            self.matching[readID] = dict()
        matchInst = self.matching[readID]
        for refInst in refMatched:
            if refInst[0] not in matchInst:
                matchInst[refInst[0]] = []
            matched = [[kPos, self.seqKmer.k], refInst[1]]
            matchInst[refInst[0]].append(matched)

    def filter_matching(self, minKmer=10, minQuotient=70):
        """remove matching instances not meeting criteria.

        Parameters
        ----------
        minKmer : int
            minimum number of kmers matching the refernce.
        minQuotient : int
            from 0 to 100 minimum\
            min percentage of sequence kmers covering the refernce from start\
            to end of the covered aread only.

        """
        emptyRef = []  # to store referenceID which no longer has matches
        k = self.seqKmer.k
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
    """combine match instances if they are in sync.

    Parameters
    ----------
    matchInst : list
        [[[kPos, k-size], refPos], [[kPos, k-size], refPos]].
    start : int
        index to start combining from.

    Returns
    -------
    (list, int)
        (list of kmers used in concatenation, number of concatenated kmers).
        ([[kPos, k-size], refPos], int)

    """
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
