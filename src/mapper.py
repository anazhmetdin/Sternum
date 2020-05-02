class mapper():
    def __init__(self, reference, sequence, trie):
        self.add_reference(reference, trie)
        self.map_sequence(sequence, trie)

    def add_reference(self, reference, trie):
        for sequenceName in reference:
            for kmer in reference[sequenceName]:
                trie.add_suffix(kmer[0], sequenceName, kmer[1])

    def map_sequence(self, sequence, trie):
        for sequenceName in sequence:
            for kmer in sequence[sequenceName]:
                trie.find_suffix(kmer[0])
