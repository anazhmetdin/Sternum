import argparse
from decode import decoder
from trie import Trie
from kmer import kmer_maker
from mapper import mapper

parser = argparse.ArgumentParser()
parser.add_argument("-m", default=1, help="Which method to use? 1:trie 2:suffi\
x array 3: bwd")
parser.add_argument("-r", default="", help="Reference file path")
parser.add_argument("-s", default="", help="Sequence reads file path")
parser.add_argument("-k", default=13, help="k-mer size")
parser.add_argument("-p", default=-1, help="patch size")
args = parser.parse_args()


def run():
    if args.m == 1:
        reference = decoder(args.r)
        sequence = decoder(args.s)
        reference_kmer = kmer_maker(int(args.k), reference, True)
        sequence_kmer = kmer_maker(int(args.k), sequence, False)
        reference_trie = Trie()
        sternum = mapper(reference_kmer, sequence_kmer, reference_trie, int(args.p))
