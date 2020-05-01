class Trie():
    def __init__(self):
        self.trie = {0:dict()}

    def add_suffix(self, suffix, sequenceName, pos):
        current_dict = self.trie[0]
        for letter in suffix:
            if letter in current_dict:
                current_dict = current_dict[letter]
            else:
                current_dict[letter] = dict()
                current_dict = current_dict[letter]
        if '$' not in current_dict:
            current_dict['$'] = []
        current_dict['$'].append([sequenceName,pos])

    def find_suffix(self, suffix):
        current_dict = self.trie[0]
        for letter in suffix:
            if letter in current_dict:
                current_dict = current_dict[letter]
            else:
                return -1
        return current_dict['$']
