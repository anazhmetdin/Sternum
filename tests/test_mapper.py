import unittest
import glob
from decode import decoder
from kmer import kmer_maker
from trie import Trie
from mapper import mapper


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
        self.assertIn("ERR1293055.19", sternum.matching)
        self.assertIn("KR233687.2.1", sternum.matching["ERR1293055.77"])
        self.assertEqual([[[0, 195], 763]], sternum.matching["ERR1293055\
.77"]["KR233687.2.1"])
        

class testMapperPatches(unittest.TestCase):

    def test_trie_insertion(self):
        """
        Test mapping case with patches
        """
        reference = decoder("data/KR233687.fasta")
        sequence = decoder("data/ERR1293055_first100.fastq")
        refKmer = kmer_maker(13, reference, True)
        seqKmer = kmer_maker(13, sequence, False)
        reference_trie = Trie()
        sternum = mapper(refKmer, seqKmer, reference_trie, 30)
        sternum.filter_matching()
        self.assertIn("ERR1293055.19", sternum.matching)
        self.assertIn("KR233687.2.1", sternum.matching["ERR1293055.77"])
        self.assertEqual([[[0, 195], 763]], sternum.matching["ERR1293055\
.77"]["KR233687.2.1"])
        files = glob.glob(seqKmer.filePrefix+"_*"+seqKmer.fileExten)
        self.assertEqual(dict(), seqKmer.kmers)
        self.assertEqual(files, [])


if __name__ == '__main__':
    unittest.main()
