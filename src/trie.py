class Trie():
    def __init__(self):
        """
trie:
{0: {A: {OTHER RECURSIVE DICTIONARIES} C: {A: {$: [[ID, pos], [ID, pos]]}}}}
        """
        self.trie = {0: dict()}

    def add_suffix(self, suffix, readID, pos):
        """
 Takes suffix = str(), readID = str(), pos = int() suffix position\
 and add each letter in suffix to "trie", which is a dictionary\
 following template:

 {0: {A: {OTHER RECURSIVE DICTIONARIES} C: {A: {$: [[ID, pos], [ID, pos]]}}}}

 each letter in the suffix represents a new dictionary, a new node, that\
 contains the following letters. When suffix ends, ['$'] is added to refere to\
 readID and pos of this suffix.
        """

        current_dict = self.trie[0]  # the first level
        for letter in suffix:
            if letter in current_dict:
                current_dict = current_dict[letter]
            else:
                current_dict[letter] = dict()
                current_dict = current_dict[letter]  # moving to the next level
        if '$' not in current_dict:
            current_dict['$'] = []
        current_dict['$'].append([readID, pos])

    def find_suffix(self, suffix):
        """
 Takes suffix = str() and search for each letter in suffix in its level'\
 dictionary, if not found it returns -1. When suffix ends, ['$'] is returned
        """
        current_dict = self.trie[0]
        for letter in suffix:
            if letter in current_dict:
                current_dict = current_dict[letter]
            else:
                return -1
        return current_dict['$']
