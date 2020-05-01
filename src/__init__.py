import argparse
from decode import *
from trie import *
from kmer import *

parser = argparse.ArgumentParser("dsfs")
parser.add_argument("-a", default=1, help="This is the 'a' variable")
args = parser.parse_args()

def run():
	print("it's still empty here")
