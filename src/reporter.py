class reporter():
    def __init__(self, sternum, filePrefix=""):
        """
 Takes sternum = mapper() and output a pseudo SAM file with limited fields\
 per match: read name, position, and read sequence
        """
        self.matching = sternum.matching
        self.sequence = sternum.seqKmer.seq.seq
        self.filePrefix = filePrefix
        self.report(filePrefix)

    def report(self, filePrefix=""):
        """
 output file to filePrefix following this pattern per line:
 read_name    None    position    None    None    None    read sequence
        """
        readName = list(self.sequence.keys())[0]
        readName = readName[: readName.find(".")]
        file = open(filePrefix+readName+".pSAM", 'w')
        lines = []
        for readID in self.matching:
            for refID in self.matching[readID]:
                for matchInst in self.matching[readID][refID]:
                    line = readID + '\tNone'
                    line += '\t' + str(matchInst[0][0] + 1)
                    line += ' ' +str(matchInst[1] + 1)
                    line += '\tNone' + '\tNone' + '\tNone'
                    line += '\t' + self.sequence[readID] + '\n'
                    lines.append(line)
        lines[-1] = lines[-1].rstrip('\n')
        file.writelines(lines)
        file.close()
