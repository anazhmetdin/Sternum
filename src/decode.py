class decoder(object):

    def __init__(self):
        self.seq = ""

    def fasta(self, fileName):
        try:
            if fileName.endswith(".fasta"):
                file = open(fileName)
            else:
                file = open("")
        except FileNotFoundError:
            print('There is no such file, make sure to write it in this\
format "XXXXX.fasta"  Try again')

        for line in file:
            line = line.rstrip()
            if not line.startswith('>'):
                self.seq += line
        file.close()

    def fastq(self, fileName):
        try:
            if fileName.endswith(".fastq"):
                file = open(fileName)
            else:
                file = open("")
        except FileNotFoundError:
            print('There is no such file, make sure to write it in this\
format "XXXXX.fastq"  Try again')

        self.seq = dict()
        for line in file:
            if line.startswith('@'):
                ID = line.lstrip('@').split(' ')
                if len(ID) > 1:
                    ID = ID[0]
                else:
                    continue
                line = file.readline()
                self.seq[ID] = []
                self.seq[ID].append(line.rstrip())
        file.close()
