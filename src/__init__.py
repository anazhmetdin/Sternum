import argparse
from decode import decoder
from trie import Trie
from sufxArr import SA
from BWT import BWT
from kmer import kmer_maker
from mapper import mapper
from reporter import reporter


parser = argparse.ArgumentParser()
parser.add_argument("-m", "--method", metavar="METHOD", default=1,
                    help="Which method to use? 1:trie 2:suffi x array 3: bwd")
parser.add_argument("-r", "--reference", metavar="REFERENCE",
                    help="Reference file path")
parser.add_argument("-s", "--sequence", metavar="SEQUENCE",
                    help="Sequence reads file path")
parser.add_argument("-k", "--ksize", metavar="KSIZE", default=13,
                    help="k-mer size")
parser.add_argument("-b", "--batchSize", metavar="BATCHSIZE", default=-1,
                    help="Batch size, if equals to -1 no batches are used")
parser.add_argument("-c", "--minKcount", metavar="MINKCOUNT", default=10,
                    help="Min allowed count of matching kmers")
parser.add_argument("-p", "--minPercentage", metavar="PERCENTAGE", default=70,
                    help="Min allowed matching similarity percentage")
parser.add_argument("-o", "--outputPrefix", metavar="OUTPUTPF", default="",
                    help="Output file prefix path")
args = parser.parse_args()


def run():
    reference = decoder(args.reference)
    sequence = decoder(args.sequence)
    if int(args.method) == 3:
        spine = BWT(reference)
        refKmer = reference
    else:
        refKmer = kmer_maker(int(args.ksize), reference, True)
    seqKmer = kmer_maker(int(args.ksize), sequence, False)
    if int(args.method) == 1:  # mapping through Suffix Trie
        spine = Trie()
    elif int(args.method) == 2:  # mapping through Suffix Array
        spine = SA(reference)
    sternum = mapper(refKmer, seqKmer, spine, int(args.batchSize))
    sternum.filter_matching(int(args.minKcount), int(args.minPercentage))
    reporter(sternum, args.outputPrefix+"_"+str(args.method)+"_")
