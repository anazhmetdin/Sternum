class mapper():
    def __init__(self, reference, sequence, trie):
        self.reference = reference
        self.sequence = sequence
        self.trie = trie
        self.add_reference()
        self.map_sequence()

    def add_reference(self):
        for sequenceName in self.reference:
            for kmer in self.reference[sequenceName]:
                self.trie.add_suffix(kmer[0], sequenceName, kmer[1])

    def map_sequence(self):
        for sequenceName in self.sequence:
            for kmer in self.sequence[sequenceName]:
                self.trie.find_suffix(kmer[0])
