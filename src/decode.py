class decoder(object):

    def __init__(self):
        self.seq = dict()

    def fasta(self, fileName):
        if fileName.endswith(".fasta"):
                file = open(fileName)
        else:
            raise FileNotFoundError('There is no such file, make sure to write it in this\
format "XXXXX.fasta"  Try again')

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
        if fileName.endswith(".fastq"):
            file = open(fileName)
        else:
            raise FileNotFoundError('There is no such file, make sure to write it in this\
format "XXXXX.fasta"  Try again')

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
