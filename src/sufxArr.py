class SA():
    """takes reference = decoder().

    Parameters
    ----------
    reference : decoder
        contains the reference that will be mapped to it.

    """
    def __init__(self, reference):
        """
sa : list:
[49, 892, 84, 4, ...]
        """
        self.sa = []
        self.reference = reference
        # index : list
        # [[readID, len], [readID, len]] for reads in reference
        self.index = [[y, len(x)] for y,x in reference.seq.items()]
        # [[readID, last pos], [readID, last pos]] for reads in reference
        for read in range(1,len(self.index)):
            self.index[read][1] += self.index[read-1][1]
        self.toBeSorted = dict()

    def add_suffix(self, suffix, pos, order=False):
        """Takes suffix and append it's position suffix array and sort SA\
         alphabtically if order = True.

        Parameters
        ----------
        suffix : str
            The suffix to be inserted in SA.
        pos : int
            suffix position.
        order : bool
            whether to order SA or not.

        """
        self.toBeSorted[suffix] = pos
        if order:
            for _, v in sorted(self.toBeSorted.items()):
                self.sa.append(v)
            self.toBeSorted.clear()

    def find_index(self, pos):
        """Short summary.

        Parameters
        ----------
        pos : type
            Description of parameter `pos`.

        Returns
        -------
        type
            Description of returned object.

        """
        for read in range(len(self.index)):
            if pos < self.index[read][1]:
                return self.index[read], read

    def comp_alph(self, m, suffix):
        """compares two strings alphabtically.

        Parameters
        ----------
        readID : str
            first string key in index
        pos : int
            first string pos in index[readID]
        suffix : str
            second string

        Returns
        -------
        int
            -1 if s1 < s2 alphabtically
            1 if s1 > s2 alphabtically
            0 if s1 = s2

        """
        pos = self.sa[m]
        read, readNum = self.find_index(pos)
        if readNum != 0:
            pos -= self.index[readNum-1][1]
        s1 = suffix
        s2 = self.reference.seq[read[0]][pos:pos+len(suffix)]
        for i in range(len(s1)):
            if ord(s1[i]) < ord(s2[i]):
                return read[0], pos, -1
            if ord(s1[i]) > ord(s2[i]):
                return read[0], pos, 1
        return read[0], pos, 0

    def find_suffix(self, suffix):
        """do a binary search using indecies stored in sa to find suffix in\
         the reference.

        Parameters
        ----------
        suffix : str()
            pattern to found in reference.

        Returns
        -------
        int or list
            -1 if pattern not found
            [[refID, kPos], [refID, kPos]] if pattern is found

        """
        """
 Takes suffix = str() and search for each letter in suffix in its level'\
 dictionary, if not found it returns -1. When suffix ends, ['$'] is returned
        """
        s = 0
        e = len(self.sa)
        while s <= e :
            m = int(s + (e - s)/2)
            readID, pos, res = self.comp_alph(m, suffix)  # readID, pos of Ref
            matches = []
            if (res == 0):
                tempM = m
                tempRes = res
                while tempRes == 0:
                    matches.append([readID, pos])
                    tempM += 1
                    readID, pos, tempRes = self.comp_alph(tempM, suffix)
                while res == 0:
                    m -= 1
                    readID, pos, res = self.comp_alph(m, suffix)
                    matches.append([readID, pos])
                matches = matches[:-1]  # delete element that broke while loop
                return matches
            if res < 0:
                e = m - 1
            else:
                s = m + 1
        return -1
