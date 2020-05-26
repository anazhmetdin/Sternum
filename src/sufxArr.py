class SA():
    """takes reference = decoder().

    Parameters
    ----------
    reference : decoder
        contains the reference that will be mapped to it.

    """

    def __init__(self, reference):
        """sa : list:
        [indecies of ordered kmers alphabtically]
        """
        self.sa = []
        self.reference = reference
        self.index = make_index(reference)
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
        read, readNum = find_index(self.index, pos)
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
        s = 0
        e = len(self.sa)-1
        while s <= e:
            m = int(s + (e - s)/2)
            readID, pos, res = self.comp_alph(m, suffix)  # readID, pos of Ref
            matches = []
            if (res == 0):
                tempM = m
                tempRes = res
                while tempRes == 0:
                    matches.append([readID, pos])
                    if tempM == len(self.sa)-1:
                        break
                    tempM += 1
                    readID, pos, tempRes = self.comp_alph(tempM, suffix)
                while res == 0:
                    m -= 1
                    if tempM == -1:
                        break
                    readID, pos, res = self.comp_alph(m, suffix)
                    matches.append([readID, pos])
                if res != 0:
                    matches = matches[:-1]
                return matches
            if res < 0:
                e = m - 1
            else:
                s = m + 1
        return -1


def make_index(reference):
    """store summary info from decoder object.

    Parameters
    ----------
    reference : decoder

    Returns
    -------
    list
        [[readID, last pos], [readID, last pos]]

    """
    # index : list
    # [[readID, len], [readID, len]] for reads in reference
    index = [[y, len(x)] for y, x in reference.seq.items()]
    # [[readID, last pos], [readID, last pos]] for reads in reference
    for read in range(1, len(index)):
        index[read][1] += index[read-1][1]
    return index


def find_index(index, pos):
    """find the read from refrence whihc pos belongs to.

    Parameters
    ----------
    pos : int
        actual pos in the whole reference
    index : list
        [[readID, last pos], [readID, last pos]]

    Returns
    -------
    list
        [[readID, last pos], readIndex]

    """
    for read in range(len(index)):
        if pos < index[read][1]:
            return index[read], read
