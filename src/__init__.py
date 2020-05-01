import argparse
from decode import *
from trie import *
from kmer import *

parser = argparse.ArgumentParser()
parser.add_argument("-m", default=1, help="Which method to use? 1:trie 2:suffix array 3: bwd")
parser.add_argument("-r", default=1, help="Reference file path")
parser.add_argument("-s", default=1, help="Sequence reads file path")
parser.add_argument("-k", default=13, help="k-mer size")
args = parser.parse_args()

def run():
	if args.m == 1:
		reference = decoder(args.r)
		sequence = decoder(args.s)
		reference_kmer = kmer_maker(args.k, True, reference.seq)
		sequence_kmer = kmer_maker(args.k, False, sequence.seq)
		reference_trie = Trie()
		for i in reference_kmer.kmers:
			for j in reference_kmer.kmers[i]:
				reference_trie.add_suffix(j)
		for i in sequence_kmer.kmers:
			for j in sequence_kmer.kmers[i]:
				if reference_trie.find_suffix(j) != -1:
					print('x')
