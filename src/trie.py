class Trie():
    """build suffix tree (trie) using dictionary.

    Attributes
    ----------
    trie : dict
{0: {A: {OTHER RECURSIVE DICTIONARIES} C: {A: {$: [[ID, pos], [ID, pos]]}}}}

    """

    def __init__(self):
        self.trie = {0: dict()}

    def add_suffix(self, suffix, readID, pos):
        """adds suffix and its pos in readID to "trie". each letter in the \
        suffix represents a new dictionary, a new node.

        Parameters
        ----------
        suffix : str
            Description of parameter `suffix`.
        readID : str
            Description of parameter `readID`.
        pos : int
            suffix position.

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
        """searches for each letter of suffix in its level dictionary.

        Parameters
        ----------
        suffix : str
            suffix to be searched for.

        Returns
        -------
        int or list
            if not found it returns -1. When suffix is found, it returns ['$'].

        """
        current_dict = self.trie[0]
        for letter in suffix:
            if letter in current_dict:
                current_dict = current_dict[letter]
            else:
                return -1
        return current_dict['$']
