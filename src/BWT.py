from operator import itemgetter
from sufxArr import make_index, find_index


class BWT():
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
        self.bwt = dict()
        self.reference = reference
        # index : list
        # [[readID, len], [readID, len]] for reads in reference
        self.index = make_index(reference)
        self.toBeSorted = dict()
        self.last2first = []

    def add_suffix(self, suffix, pos, seq="", order=False):
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
        self.bwt = dict()
        self.last2first = []
        if order:
            self.toBeSorted.pop(suffix)
            self.toBeSorted[suffix] = pos
            sa = []
            for _, v in sorted(self.toBeSorted.items()):
                sa.append(v)
            self.toBeSorted.clear()
            n = len(seq)
            for i in sa:
                self.bwt[+((i+n-1) % n)] = (seq)[(i+n-1) % n]
                select = itemgetter(1)
                BV = self.bwt.values()
            del seq
            first2last = sorted([(i, x) for i, x in enumerate(BV)], key=select)
            self.last2first = [None for i in range(len(self.bwt))]
            for firstIndex, Xtuples in enumerate(first2last):
                lastIndex, _ = Xtuples
                self.last2first[lastIndex] = firstIndex

    def find_suffix(self, suffix):
        """search in BWT through back and fourth search.

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
        sf = 0
        ef = len(self.bwt)-1
        # print(self.bwt)
        sl = sf
        el = ef
        while sf <= ef:
            symbol = suffix[-1]
            suffix = suffix[: -1]
            lastV = list(self.bwt.values())
            if symbol in lastV[sf:ef+1]:
                sl = sf + lastV[sf:ef+1].index(symbol)
                el = ef - lastV[sf:ef+1][::-1].index(symbol)
                sf = self.last2first[sl]
                ef = self.last2first[el]
            else:
                return -1
            if suffix == "":
                matches = []
                for i in range(sl, el+1):
                    actualPos = list(self.bwt.keys())[i]
                    read, readNum = find_index(self.index, actualPos)
                    pos = list(self.bwt.keys())[i]
                    if readNum != 0:
                        pos -= self.index[readNum-1][1]
                    matches.append([read[0], pos])
                return matches
        return -1
