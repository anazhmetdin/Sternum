import unittest
from decode import decoder


class testDecoder(unittest.TestCase):
    def test_fasta(self):
        """
        Test if properly decoded
        """
        fileName = "data/KR233687.fasta"
        fastaFile = decoder(fileName)
        result = fastaFile.seq

        expected = "GAGATCTAATGTCTCAATCCCGCACTCGCGAGATACTAACAAAAACCACTGTGGACCA\
TATGGCCATAATCAAGAAATACACATCAGGAAGACAAGAGAAGAACCCTGCTCTCAGAATGAAATGGATGATGGCAAT\
GAAATATCCAATCACAGCAGACAAGAGAATAATGGAAATGATTCCTGAAAGAAATGAACAAGGCCAGACGCTTT\
GGAGCAAGACAAATGATGCTGGATCAGACAGAGTGATGGTGTCTCCCCTAGCTGTAACTTGGTGGAATAG"

        self.assertIn(expected, result["KR233687.2.1"])

        expected = "GGAGTGGAATCTGCAGTGCTGAGGGGGTTCCTAATTCTGGGCAGGGAGGACAGAAGA\
TATGGACCAGCACTAAGCATCAATGAACTGAGCAATCTTGCGAAAGGGGAGAAAGCCAATGTGCTGATAGGGCAAGG\
AGACGTGGTGCTGGTAATGAAACGGAAACGGGACTCTAGCATACTTACTGACAGCCAGACAGCGACCAAAAGAATT\
CGGATGGTCATCAATT"

        self.assertIn(expected, result["KR233687.2.2"])

    def test_fastq(self):
        """
        Test if properly decoded
        """
        fileName = "data/ERR1293055_first100.fastq"
        fastaFile = decoder(fileName)
        result = fastaFile.seq

        expected = "CTCTTCTACTTCTACACCTAATACATCCCCTCCCTCCCTCTCCCCCCTCCCCCTTCCT"
        self.assertIn(expected, str(result["ERR1293055.1"]))

        expected = "CACCCTTTCTTTATCCTTTTTATTTCTAATCTTTTTTTGTCGTTTCGTCTTTTTTTTT"
        self.assertIn(expected, str(result["ERR1293055.15"]))

        expected = "ATACAAAGCAAATCAAGGCAAAATAATTGGCCGAACAGATGTTAGCTTTAGTGGAGGA"
        self.assertIn(expected, str(result["ERR1293055.99"]))


if __name__ == '__main__':
    unittest.main()
