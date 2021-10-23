import os
import glob


class kmer_maker(object):
    """
    process reads to get kmers and store them in "kmers".

    Attributes
    ----------
    kmers : dict
        {readID.1: [["kmer", kPos], ["kmer", kPos], ..., ["kmer", kPos]]
         readID.2: [["kmer", kPos], ["kmer", kPos], ..., ["kmer", kPos]]
         .
         .
         .
         readIDn: [["kmer", kPos], ["kmer", kPos], ..., ["kmer", kPos]]}

    Parameters
    ----------
    k : int
        k size.
    seq : decoder
        reference to the original sequence.
    overlapping : bool
        if True kmers overlapp, else they don't

    """

    def __init__(self, k, seq, overlapping=True):
        """process reads to get kmers and store them in "kmers".

        Parameters
        ----------
        k : int
            k size.
        seq : decoder
            reference to the original sequence.
        overlapping : bool
            if True kmers overlapp, else they don't

        """
        self.kmers = dict()
        self.seqCount = 0
        self.k = k
        self.seq = seq
        self.filePrefix = seq.filePrefix
        self.currentBatch = 0
        self.fileExten = ".kmers"
        self.splice(self.seq.seq, overlapping)

    def splice(self, seq, overlapping):
        """process the sequence.

        Parameters
        ----------
        seq : dict
            {readID.1: "sequence",
             readID.2: "sequence"
             .
             .
             .
             readIDn: "sequence"}
        overlapping : bool
            if True kmers overlapp, else they don't
        """
        if overlapping:
            step = 1
        else:
            step = self.k
        for readID in seq:
            self.seqCount += 1
            if readID not in self.kmers:
                self.kmers[readID] = []
            for i in range(0, len(seq[readID])-self.k+1, step):
                self.kmers[readID].append([seq[readID][i:i+self.k], i])

    def dump(self, filePrefix=""):
        """
        store the processed kmers on hard disk and free the memory.

        Parameters
        ----------
        filePrefix : str
            The kmers are stored in files named as:
            filePrefix_i_readID.fileExtension

        """
        i = 0
        fileExten = self.fileExten
        if len(self.kmers) == self.seqCount:
            for readID in self.kmers:
                file = open(filePrefix+"_"+str(i)+"_"+readID+fileExten, "w")
                for kmer in self.kmers[readID]:
                    file.write(kmer[0]+'\t'+str(kmer[1])+'\n')
                i += 1
                file.close()
        self.kmers.clear()

    def load(self, filePrefix="", batchSize=-1):
        """
        load kmers stored on hard disk to the memory.

        Parameters
        ----------
        filePrefix : str
            The kmers are stored in files named as:
            filePrefix_i_readID.fileExtension.
        batchSize : int
            number of files to be loaded. if -1, then, load all files.fileExten

        """
        fileExten = self.fileExten
        flag = False  # detect if this is the last batch
        if batchSize <= 0:
            batchSize = self.seqCount-self.currentBatch
        if self.currentBatch+batchSize > self.seqCount:
            batchSize = self.seqCount-self.currentBatch
            flag = True
        for i in range(self.currentBatch, self.currentBatch+batchSize):
            for filename in glob.glob(filePrefix+"_"+str(i)+"_*"+fileExten):
                file = open(filename, 'r')
                seqPos = filename.rfind("_")
                readID = filename[seqPos+1:-len(fileExten)]
                self.kmers[readID] = []
                lines = file.readlines()
                for line in lines:
                    line = line.rstrip('\n').split('\t')
                    self.kmers[readID].append([line[0], int(line[1])])
                file.close()
        self.currentBatch += batchSize
        if flag:
            self.clear(True, filePrefix)
            return flag  # would be usefule to be used in external conditions

    def clear(self, admin=True, filePrefix=""):
        """
        remove kmers stored on hard disk and clear "kmers" from memory.

        Parameters
        ----------
        admin : bool
            if True deletes all data without asking the user.
        filePrefix : str
            The kmers are stored in files named as:
            filePrefix_i_readID.fileExtension.

        """
        fileExten = self.fileExten
        if not admin:
            print("WARNING: This will delete ALL kmers files and ALL stored\
 kmers in memory")
            opt = input("Do you wish to procceed? [y/n]: ")
        else:
            opt = 'y'
        if opt == 'y':
            for filename in glob.glob(filePrefix+"*"+fileExten):
                os.remove(filename)
            self.kmers.clear()
