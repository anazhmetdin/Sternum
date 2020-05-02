import argparse
from decode import decoder
from trie import Trie
from kmer import kmer_maker
from mapper import mapper

parser = argparse.ArgumentParser()
parser.add_argument("-m", default=1, help="Which method to use? 1:trie 2:suffi\
x array 3: bwd")
parser.add_argument("-r", default=1, help="Reference file path")
parser.add_argument("-s", default=1, help="Sequence reads file path")
parser.add_argument("-k", default=13, help="k-mer size")
args = parser.parse_args()


def run():
    if args.m == 1:
        reference = decoder(args.r)
        sequence = decoder(args.s)
        reference_kmer = kmer_maker(int(args.k), reference.seq, True)
        sequence_kmer = kmer_maker(int(args.k), sequence.seq, False)
        reference_trie = Trie()
        sternum = mapper(reference_kmer.kmers, sequence_kmer.kmers, reference_trie)
