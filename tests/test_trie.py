import unittest
from trie import Trie


class testTrie(unittest.TestCase):

    global names
    names = Trie()

    def test_trie_insertion(self):
        """
        Test if elements are added in correct hirachy
        """
        global names
        names.add_suffix("Ahmed", 5, 1)
        names.add_suffix("Abdullah", 8, 2)
        names.add_suffix("Omar", 4, 3)
        names.add_suffix("Sarah", 5, 4)
        names.add_suffix("Oman", 4, 5)
        result = len(names.trie[0])
        result1 = len(names.trie[0]['A'])
        result2 = len(names.trie[0]['O']['m'])
        result3 = list(names.trie[0]['O']['m']['a'].keys())

        self.assertEqual(result, 3)
        self.assertEqual(result1, 2)
        self.assertEqual(result2, 1)
        self.assertEqual(result3, ['r', 'n'])

    def test_trie_searching(self):
        """
        Test if patterns are read after addition
        """
        global names
        result = names.find_suffix('Ahmed')
        result1 = names.find_suffix('Abdullah')
        result2 = names.find_suffix('Omar')

        self.assertEqual(result, [[5, 1]])
        self.assertEqual(result1, [[8, 2]])
        self.assertEqual(result2, [[4, 3]])


if __name__ == '__main__':
    unittest.main()
