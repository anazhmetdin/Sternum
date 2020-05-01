import unittest
from kmer import *
from decode import *

class testKmer(unittest.TestCase):

    def test_splice_fasta_overlapping(self):
        """
        Test splicing fasta overlapping kmers
        """
        fileName = "data/KR233687.fasta"
        fastaFile = decoder()
        fastaFile.fasta(fileName)
        kmer = kmer_maker(13, True, fastaFile.seq)
        self.assertIn("GAGATCTAATGTC", kmer.kmers["KR233687.2.1"])
        self.assertIn("TAATGGTGGCATA", kmer.kmers["KR233687.2.1"])
        self.assertIn("ATTCAGTTGATAG", kmer.kmers["KR233687.2.2"])
        self.assertIn("ATGGTCATCAATT", kmer.kmers["KR233687.2.2"])
        self.assertEqual(2, kmer.seqCount)

    def test_splice_fasta_Nonoverlapping(self):
        """
        Test splicing fasta nonoverlapping kmers
        """
        fileName = "data/KR233687.fasta"
        fastaFile = decoder()
        fastaFile.fasta(fileName)
        kmer = kmer_maker(13, False, fastaFile.seq)
        self.assertIn("GAGATCTAATGTC", kmer.kmers["KR233687.2.1"])
        self.assertIn("TCAATCCCGCACT", kmer.kmers["KR233687.2.1"])
        self.assertIn("TTCGGATGGTCAT", kmer.kmers["KR233687.2.2"])
        self.assertNotIn("AGATCTAATGTCT", kmer.kmers["KR233687.2.1"])
        self.assertEqual(2, kmer.seqCount)

    def test_splice_fastq_overlapping(self):
        """
        Test splicing fastq overlapping kmers
        """
        fileName = "data/ERR1293055_first100.fastq"
        fastaFile = decoder()
        fastaFile.fastq(fileName)
        kmer = kmer_maker(13, True, fastaFile.seq)
        self.assertIn("TCCTCTTTCTTTC", kmer.kmers["ERR1293055.5"])
        self.assertIn("GTTGGGATCAATA", kmer.kmers["ERR1293055.40"])
        self.assertIn("CTCTTCTACTTCT", kmer.kmers["ERR1293055.1"])
        self.assertIn("TCAAATGTTCCTT", kmer.kmers["ERR1293055.100"])
        self.assertEqual(100, kmer.seqCount)

    def test_splice_fastq_Nonoverlapping(self):
        """
        Test splicing fastq nonoverlapping kmers
        """
        fileName = "data/ERR1293055_first100.fastq"
        fastaFile = decoder()
        fastaFile.fastq(fileName)
        kmer = kmer_maker(13, False, fastaFile.seq)
        self.assertIn("CTCTTCTACTTCT", kmer.kmers["ERR1293055.1"])
        self.assertIn("GTTGGGATCAATA", kmer.kmers["ERR1293055.40"])
        self.assertIn("ATTCAAATGTTCC", kmer.kmers["ERR1293055.100"])
        self.assertNotIn("TCCACTTCACTTT", kmer.kmers["ERR1293055.90"])
        self.assertEqual(100, kmer.seqCount)

    def test_dump(self):
        """
        Test storing kmers to disk
        """
        fileName = "data/ERR1293055_first100.fastq"
        fastaFile = decoder()
        fastaFile.fastq(fileName)
        kmer = kmer_maker(13, False, fastaFile.seq)
        kmer.dumb()
        file = open("_39_ERR1293055.40.kmers")
        lines = file.read()
        self.assertIn("GTTGGGATCAATA", lines)
        file.close()

    def test_load(self):
        """
        Test storing kmers to disk
        """
        fileName = "data/ERR1293055_first100.fastq"
        fastaFile = decoder()
        fastaFile.fastq(fileName)
        kmer = kmer_maker(13, False, fastaFile.seq)
        kmer.dumb()
        result = kmer.load("", 3)
        self.assertIn("CTCCCTCTCCCCT", result["ERR1293055.3"])

    def test_zclear(self):
        """
        Test deleting kmers' files from disk
        """
        fileName = "data/ERR1293055_first100.fastq"
        fastaFile = decoder()
        fastaFile.fastq(fileName)
        kmer = kmer_maker(13, False, fastaFile.seq)
        kmer.dumb()
        kmer.clear()
        self.assertEqual(dict(), kmer.kmers)

if __name__ == '__main__':
    unittest.main()
