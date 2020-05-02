import os


class decoder(object):

    def __init__(self, fileName):
        self.seq = dict()
        if fileName.endswith(".fasta"):
            self.fasta(fileName)
        else:
            self.fastq(fileName)

    def fasta(self, fileName):
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
