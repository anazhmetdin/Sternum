import unittest
import os
from decode import decoder
from kmer import kmer_maker
from trie import Trie
from mapper import mapper
from reporter import reporter


class testMapperNoPatches(unittest.TestCase):

    def test_trie_insertion(self):
        """
        Test mapping case with no patches
        """
        reference = decoder("data/KR233687.fasta")
        sequence = decoder("data/ERR1293055_first100.fastq")
        refKmer = kmer_maker(13, reference, True)
        seqKmer = kmer_maker(13, sequence, False)
        reference_trie = Trie()
        sternum = mapper(refKmer, seqKmer, reference_trie, -1)
        sternum.filter_matching()
        reporter(sternum)
        file = open("ERR1293055.pSAM")
        line = file.readline()
        file.close()
        self.assertIn("ERR1293055.19	None	14 728	None	None	None\
	CTGGCGGAGAAGTGAGAAAT", line)
        os.remove("ERR1293055.pSAM")


if __name__ == '__main__':
    unittest.main()
