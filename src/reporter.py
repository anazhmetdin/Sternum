class reporter():
    """

    generate pseudo SAM files.

    Parameters
    ----------
    sternum : mapper
        mpper object having matches.
    filePrefix : str
        file path prefix of output file.

    """

    def __init__(self, sternum, filePrefix=""):
        """
        output a pseudo SAM file with limited fields\
        per match: read name, position, and read sequence.

        Parameters
        ----------
        sternum : mapper
            mpper object having matches.
        filePrefix : str
            file path prefix of output file.

        """
        self.matching = sternum.matching
        self.sequence = sternum.seqKmer.seq.seq
        self.filePrefix = filePrefix
        self.report(filePrefix)

    def report(self, filePrefix=""):
        """
        output file to filePrefix following this pattern per line:
        read_name    None    position    None    None    None    read sequence

        Parameters
        ----------
        filePrefix : str
            file path prefix of output file.

        """
        readName = list(self.sequence.keys())[0]
        readName = readName[: readName.find(".")]
        file = open(filePrefix+readName+".sam", 'w')
        lines = []
        for readID in self.matching:
            for refID in self.matching[readID]:
                for matchInst in self.matching[readID][refID]:
                    line = readID + '\t0'
                    line += '\t' + refID
                    line += '\t' + str(matchInst[1] + 1)
                    line += '\t255' + '\t*' + '\t*' + '\t0'
                    line += '\t' + self.sequence[readID]
                    line += '\t*' + '\n'
                    lines.append(line)
        lines[-1] = lines[-1].rstrip('\n')
        file.writelines(lines)
        file.close()
