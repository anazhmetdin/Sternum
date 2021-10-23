import os


class decoder(object):
    """
    store reads.

    Parameters
    ----------
    fileName : str
        file path to be decoded.

    Attributes
    ----------
    seq : dict
        {readID.1: "sequence",
         readID.2: "sequence"
         .
         .
         .
         readIDn: "sequence"}
    filePrefix : string
        file path where additional file will be saved

    """

    def __init__(self, fileName):
        """
        automatically detect file type and extract reads.

        Parameters
        ----------
        fileName : type
            file path that will be decoded.

        """
        self.seq = dict()
        self.filePrefix = fileName[:fileName.rfind("\\")+1]
        if fileName.endswith(".fasta"):
            self.fasta(fileName)
        else:
            self.fastq(fileName)

    def fasta(self, fileName):
        """
        Takes the fasta file path "XXXXX.fasta"and  extract\
        the sequence and store it in "seq".

        Parameters
        ----------
        fileName : str
            file path that will be decoded.

        """
        if fileName.endswith(".fasta") and os.path.exists(fileName):
            file = open(fileName)
        else:
            raise FileNotFoundError('make sure the file exists and write it in\
 this format "XXXXX.fasta" or "XXXXX.fastq" Try again')

        for line in file:
            if line.startswith('>'):
                line = line.lstrip('>')
                ID = line.split(' ')[0]
                self.seq[ID] = ""
            else:
                line = line.rstrip()
                self.seq[ID] += line
        file.close()

    def fastq(self, fileName):
        """Takes the fasta file path "XXXXX.fasta"and  extract\
        the sequence and store it in "seq".

        Parameters
        ----------
        fileName : str
            file path that will be decoded.

        """
        if fileName.endswith(".fastq") and os.path.exists(fileName):
            file = open(fileName)
        else:
            raise FileNotFoundError('make sure the file exists and write it in\
 this format "XXXXX.fasta" or "XXXXX.fastq" Try again')

        for line in file:
            if line.startswith('@'):
                ID = line.lstrip('@').split(' ')
                if len(ID) > 1:
                    ID = ID[0]
                else:
                    continue
                line = file.readline()
                self.seq[ID] = line.rstrip()
        file.close()
