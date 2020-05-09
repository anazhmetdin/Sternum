import unittest
import os
from reporter import reporter
from tests.test_mapper import initiate_case


class testMapperNoPatches(unittest.TestCase):

    def test_trie_insertion(self):
        """
        Test mapping case with no patches
        """
        sternum = initiate_case(-1)
        reporter(sternum)
        file = open("ERR1293055.pSAM")
        line = file.readline()
        file.close()
        self.assertIn("ERR1293055.19\tNone\t14 728\tNone\tNone\tNone\
\tCTGGCGGAGAAGTGAGAAAT", line)
        os.remove("ERR1293055.pSAM")


if __name__ == '__main__':
    unittest.main()
