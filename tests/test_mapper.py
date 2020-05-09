import unittest
from decode import decoder
from kmer import kmer_maker
from trie import Trie
from mapper import mapper


class testMapper(unittest.TestCase):

    def test_mapper_no_patches(self):
        """
        Test mapping case with no patches
        """
        sternum = initiate_case(-1)
        self.assertIn("ERR1293055.19", sternum.matching)
        self.assertIn("KR233687.2.1", sternum.matching["ERR1293055.77"])
        self.assertEqual([[[0, 195], 763]], sternum.matching["ERR1293055\
.77"]["KR233687.2.1"])

    def test_mapper_patches(self):
        """
        Test mapping case with patches
        """
        sternum = initiate_case(30)
        self.assertIn("ERR1293055.77", sternum.matching)
        self.assertIn("KR233687.2.1", sternum.matching["ERR1293055.19"])
        self.assertEqual([[[13, 221], 727]], sternum.matching["ERR1293055\
.19"]["KR233687.2.1"])


def initiate_case(patchSize):
    reference = decoder("data/KR233687.fasta")
    sequence = decoder("data/ERR1293055_first100.fastq")
    refKmer = kmer_maker(13, reference, True)
    seqKmer = kmer_maker(13, sequence, False)
    reference_trie = Trie()
    sternum = mapper(refKmer, seqKmer, reference_trie, patchSize)
    sternum.filter_matching()
    return sternum


if __name__ == '__main__':
    unittest.main()
