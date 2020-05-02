import os
import glob


class kmer_maker(object):
    def __init__(self, k, overlapping=True, seq=dict()):
        self.kmers = dict()
        self.seqCount = 0
        self.k = k
        self.splice(seq, overlapping)

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

    def dumb(self, filePrefix=""):
        i = 0
        for sequence in self.kmers:
            file = open(filePrefix+"_"+str(i)+"_"+sequence+".kmers", "a")
            for kmer in self.kmers[sequence]:
                file.write(kmer[0]+'\t'+str(kmer[1])+'\n')
            i += 1
            file.close()

    def load(self, filePrefix="", patchSize=1):
        currentPatch = 0
        if os.path.exists("patch.kmers"):
            file = open("patch.kmers")
            currentPatch = int(file.read().rstrip())
            file.close()
        else:
            file = open("patch.kmers", 'a')
            file.write(str(currentPatch))
            file.close()

        self.kmers = dict()
        for i in range(currentPatch, currentPatch+patchSize):
            for filename in glob.glob(filePrefix+"_"+str(i)+"_*.kmers"):
                with open(filename, 'r') as file:
                    seqPos = filename.rfind("_")
                    sequence = filename[seqPos+1:-6]
                    self.kmers[sequence] = []
                    for line in file:
                        line = line.rstrip('\n')
                        self.kmers[sequence].append(line.split('\t'))

        file = open("patch.kmers", 'w')
        file.write(str(currentPatch+patchSize))
        file.close()
        return self.kmers

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
