import os
import glob


class kmer_maker(object):
    def __init__(self, k, seq, overlapping=True):
        self.kmers = dict()
        self.seqCount = 0
        self.k = k
        self.seq = seq
        self.splice(self.seq.seq, overlapping)

    def splice(self, seq, overlapping):
        if overlapping:
            step = 1
        else:
            step = self.k
        for sequence in seq:
            self.seqCount += 1
            if sequence not in self.kmers:
                self.kmers[sequence] = []
            for i in range(0, len(seq[sequence])-self.k+1, step):
                self.kmers[sequence].append([seq[sequence][i:i+self.k], i])

    def dump(self, filePrefix=""):
        i = 0
        for sequence in self.kmers:
            file = open(filePrefix+"_"+str(i)+"_"+sequence+".kmers", "a")
            for kmer in self.kmers[sequence]:
                file.write(kmer[0]+'\t'+str(kmer[1])+'\n')
            i += 1
            file.close()

    def load(self, filePrefix="", patchSize=-1):
        currentPatch = 0
        flag = False
        if os.path.exists(filePrefix+"patch.kmers"):
            file = open(filePrefix+"patch.kmers")
            currentPatch = int(file.read().rstrip())
            file.close()
        else:
            file = open(filePrefix+"patch.kmers", 'a')
            file.write(str(currentPatch))
            file.close()
        if patchSize == -1:
            patchSize = self.seqCount-currentPatch
        self.kmers = dict()
        if currentPatch+patchSize > self.seqCount:
            patchSize = self.seqCount-currentPatch
            flag = True
        for i in range(currentPatch, currentPatch+patchSize):
            for filename in glob.glob(filePrefix+"_"+str(i)+"_*.kmers"):
                with open(filename, 'r') as file:
                    seqPos = filename.rfind("_")
                    sequence = filename[seqPos+1:-6]
                    self.kmers[sequence] = []
                    for line in file:
                        line = line.rstrip('\n').split('\t')
                        self.kmers[sequence].append([line[0], int(line[1])])

        file = open(filePrefix+"patch.kmers", 'w')
        file.write(str(currentPatch+patchSize))
        file.close()
        if flag:
            self.clear(True, filePrefix)
            return flag

    def clear(self, admin=True, filePrefix=""):
        if not admin:
            print("WARNING: This will delete ALL kmers files and ALL stored\
 kmers in memory")
            opt = input("Do you wish to procceed? [y/n]: ")
        else:
            opt = 'y'
        if opt == 'y':
            for filename in glob.glob(filePrefix+"*"+".kmers"):
                os.remove(filename)
            self.kmers = dict()
