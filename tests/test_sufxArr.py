import unittest
from sufxArr import SA


class pseudpRef():
    def __init__(self, pseq):
        self.seq = pseq


class testSufxArr(unittest.TestCase):

    global names
    names = SA(pseudpRef({1: 'AhmedOmarSarah', 2: 'AbdullahOman'}))

    def test_SA_insertion(self):
        """
        Test if elements are added in correct hirachy
        """
        names.add_suffix("Ahmed", 0)
        names.add_suffix("Abdullah", 14)
        names.add_suffix("Omar", 5)
        names.add_suffix("Sarah", 9)
        names.add_suffix("Oman", 22)
        names.add_suffix("Oman", 22, True)
        result = len(names.sa)
        result1 = names.sa[0]
        self.assertEqual(result, 5)
        self.assertEqual(result1, 14)

    def test_SA_searching(self):
        """
        Test if patterns are read after addition
        """
        self.assertEqual(names.find_suffix('Ahmed'), [[1, 0]])


if __name__ == '__main__':
    unittest.main()
