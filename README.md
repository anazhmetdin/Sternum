
# Sternum [![Codacy Badge](https://api.codacy.com/project/badge/Grade/ac863680dcac4a2ba90672a9778ebf29)](https://www.codacy.com/manual/anegm98/sternum?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=anegm98/sternum&amp;utm_campaign=Badge_Grade)[![Build Status](https://travis-ci.org/anegm98/Sternum.svg?branch=master)](https://travis-ci.org/github/anegm98/Sternum)

# description

Sternum is a python package that map Next Generation Sequencing reads to a reference geneome using different algorithms and data structures.


## Available methods

### 1. Suffix Tree (Trie):
 ![Example from: http://btechsmartclass.com/data_structures/tries.html](https://imgur.com/kkHmEla.png)
######  *Example from: http://btechsmartclass.com/data_structures/tries.html*

`trie` is implemented using dictionaries in python. Each node represents one nucleotide and points to a new dictionary for the followong nucleotide. The last charcter of any suffix is **'$'** points to a list of information about readID and position of this suffix

>{0: {A: {OTHER RECURSIVE DICTIONARIES} C: {A: {$: [[ID, pos], [ID, pos]]}}}}

To find a pattern in `trie`	 , the pattern is matched against the trie letter by letter untill it reaches **'$'**.  If the pattern fails to reach a trie leaf it returns **-1**, else, **[ID, pos]**

 `trie` is constructed from *m* genome in linear time **O(|*m*|)** and each pattern *n* is found in linear time **O(|*n*|)**

### 2. Suffix Array (SA)
 ![Example from: https://discuss.codechef.com/t/a-tutorial-on-suffix-arrays/2950](https://imgur.com/pYDBPu5.png)
 ######  *Example from:  https://discuss.codechef.com/t/a-tutorial-on-suffix-arrays/2950*

 `sa` is implemented using list in python. Each index points to ith order kmer in the whole reference.
 >[indecies of ordered kmers alphabtically]

 To find a pattern in `sa`	 , binary search is performed using these indecies since the kmers are ordered. the pattern is matched each time against the kmer selected by binary seach untill it reaches a match.  If the pattern fails to reach a match it returns **-1**, else, **[ID, pos]**

  `sa` is constructed from *m* genome in logarithmic time **O(|*m.log(m)*|)** and each pattern *n* is found in logarithmic time **O(|*m*|.log(|*m*|))** , however, it's stored in much less memory size than `trie`

### 3. Burrow Wheeler Transform (BWT)
![Example from: Zhang, D., Liu, Q., Wu, Y., Li, Y., & Xiao, L. (2013). Compression and Indexing Based on BWT: A Survey. _2013 10Th Web Information System And Application Conference_. doi: 10.1109/wisa.2013.20](https://imgur.com/ISi1vjt.png)
 ######  *Example from:  Zhang, D., Liu, Q., Wu, Y., Li, Y., & Xiao, L. (2013). Compression and Indexing Based on BWT: A Survey. _2013 10Th Web Information System And Application Conference_. doi: 10.1109/wisa.2013.20*
 `bwt` is implemented using list and dictionary in python. Each index points to a suffix in the whole reference.
 >{index: 'nucleotide', index: 'nucleotide', ..., index: '$', ..., index: 'nucleotide'}

 along with last2first list to point to this suffix in a column of ordered suffixes, which necessary to search for pattern through going back and forth from BWT to the first column.
 ![Example from: Rocha, M., & Ferreira, P. Bioinformatics Algorithms (p. 357).](https://i.imgur.com/P1SnN3e.png)
 ######  *Example from:  Rocha, M., & Ferreira, P. Bioinformatics Algorithms (p. 357)*

 To find a pattern in `bwt` , back and forth walk through the inverted pattern in the first and last column. the pattern is matched if it reaches its first character in the last column.  If the pattern fails to reach a match it returns **-1**, else, **[ID, pos]**

  `bwt` is constructed from *m* genome in logarithmic time **O(|*m*|.log(|*m*|))** and each pattern *n* is found in linear time **O(|*n*|)**.


## Input and Output

###  Input:
 - #### Reference genome file `-r` str()
fasta/fastq file
- #### Sequence reads file `-s` str()
fasta/fastq file. *paired reads are not supported*
- #### kmer size `-k` int()
smaller kmer size means more allowance for mismatches
- #### Minimum count of matched kmers `-c`int()
minimum allowed number of kmers matching the reference in sequence to be reported.
- #### Minimum matching percentage `-p` int()
minimum allowed percentage of similarity between matched part of read and covered stretch of genome
- #### Batch size `-b` int()
how many sequence reads to be loaded into memory per iteration to be mapped

###  Output:

- #### pseudo SAM file `-o` str()
a file containing only read name, position, and read sequence per match

## Getting started

### Installing the package

- Download the latest release: [releases](https://github.com/anegm98/Sternum/releases)

- In your command line environment:

		pip install path/to/sternum-x.x.x-py2.py3-none-any.whl

### Run an example

- In your Command Line environment:

		sternum -m method -r path/to/reference.fastx -s path/to/sequence.fastx -k kmerSize -p minPercentage -c minKcount -b batchSize -o path/to/myfirstmap

- this file will be genrated:
path/to/myfirstmap_\$m_\$sequenceID.pSAM

- you can try with files in [sternum/data](https://github.com/anegm98/Sternum/tree/master/data)
