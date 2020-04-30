import argparse
from hi import *

parser = argparse.ArgumentParser("dsfs")
parser.add_argument("-a", default=1, help="This is the 'a' variable")
args = parser.parse_args()

def run():
	func()
