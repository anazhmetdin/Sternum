class mapper():
    def __init__(self, reference, sequence, trie, patch=-1):
        self.reference = reference
        self.sequence = sequence
        self.trie = trie
        self.patch = patch
        self.matching = dict()
        self.add_reference()
        self.map_sequence(self.patch)

    def add_reference(self):
        for sequenceName in self.reference.kmers:
            for kmer in self.reference.kmers[sequenceName]:
                self.trie.add_suffix(kmer[0], sequenceName, kmer[1])

    def map_sequence(self, patch=-1):
        if patch == -1:
            for sequenceName in self.sequence.kmers:
                for kmer in self.sequence.kmers[sequenceName]:
                    refMatched = self.trie.find_suffix(kmer[0])
                    if refMatched != -1:
                        self.match(sequenceName, kmer[1], refMatched)
        else:
            self.sequence.dump(self.sequence.seq.filePrefix)
            if self.sequence.load(self.sequence.seq.filePrefix, self.patch):
                return
            self.map_sequence()
            self.map_sequence(self.patch)
