import unittest
from trie import *

class testTrie(unittest.TestCase):

    global names
    names = Trie()

    def test_trie_insertion(self):
        """
        Test if elements are added in correct hirachy
        """
        global names
        names.add_suffix("Ahmed")
        names.add_suffix("Abdullah")
        names.add_suffix("Omar")
        names.add_suffix("Sarah")
        names.add_suffix("Oman")
        result = len(names.trie[0])
        result1 = len(names.trie[0]['A'])
        result2 = len(names.trie[0]['O']['m'])
        result3 = list(names.trie[0]['O']['m']['a'].keys())

        self.assertEqual(result, 3)
        self.assertEqual(result1, 2)
        self.assertEqual(result2, 1)
        self.assertEqual(result3, ['r','n'])

    def test_trie_searching(self):
        """
        Test if patterns are read after addition
        """
        global names
        result = names.find_suffix('Ahmed')
        result1 = names.find_suffix('Abdullah')
        result2 = names.find_suffix('Omar')

        self.assertEqual(result, 5)
        self.assertEqual(result1, 8)
        self.assertEqual(result2, 4)

if __name__ == '__main__':
    unittest.main()
