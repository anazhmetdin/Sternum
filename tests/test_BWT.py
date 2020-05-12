import unittest
from BWT import BWT


class pseudpRef():
    def __init__(self, pseq):
        self.seq = pseq


class testBWT(unittest.TestCase):

    global names
    names = BWT(pseudpRef({1: 'TAGACAGAGA'}))

    def test_BWT_insertion(self):
        """
        Test if elements are added in correct hirachy
        """
        names.add_suffix("$", 10)
        names.add_suffix("A$", 9)
        names.add_suffix("GA$", 8)
        names.add_suffix("AGA$", 7)
        names.add_suffix("GAGA$", 6)
        names.add_suffix("AGAGA$", 5)
        names.add_suffix("CAGAGA$", 4)
        names.add_suffix("ACAGAGA$", 3)
        names.add_suffix("GACAGAGA$", 2)
        names.add_suffix("AGACAGAGA$", 1)
        names.add_suffix("TAGACAGAGA$", 0, 'TAGACAGAGA$', True)
        result = len(names.bwt)
        result1 = names.bwt[1]
        result2 = names.bwt[2]
        self.assertEqual(result, 11)
        self.assertEqual(result1, 'A')
        self.assertEqual(result2, 'G')

    def test_BwD_searching(self):
        """
        Test if patterns are read after addition
        """
        self.assertEqual(names.find_suffix('ACA'), [[1, 3]])


if __name__ == '__main__':
    unittest.main()
