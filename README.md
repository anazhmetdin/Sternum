# Sternum [![Codacy Badge](https://app.codacy.com/project/badge/Grade/b568df08e6f44544b4e0aac5f9398513)](https://www.codacy.com/gh/anazhmetdin/Sternum/dashboard?utm_source=github.com&utm_medium=referral&utm_content=anazhmetdin/Sternum&utm_campaign=Badge_Grade)[![Build Status](https://travis-ci.org/anazhmetdin/Sternum.svg?branch=master)](https://travis-ci.org/github/anazhmetdin/Sternum)

## description

Sternum is a python package that map Next Generation Sequencing reads to a reference geneome using different algorithms and data structures.

## Available methods

### 1. Suffix Tree (Trie)

![](https://imgur.com/kkHmEla.png)

Example from: http://btechsmartclass.com/data_structures/tries.html

`trie` is implemented using dictionaries in python. Each node represents one nucleotide and points to a new dictionary for the followong nucleotide. The last charcter of any suffix is **'$'** points to a list of information about readID and position of this suffix

> {0: {A: {OTHER RECURSIVE DICTIONARIES} C: {A: {$: \[\[ID, pos\], \[ID, pos\]\]}}}}

To find a pattern in `trie` , the pattern is matched against the trie letter by letter untill it reaches **'$'**. If the pattern fails to reach a trie leaf it returns **-1**, else, **[ID, pos]**

`trie` is constructed from _m_ genome in linear time **O(|_m_|)** and each pattern _n_ is found in linear time **O(|_n_|)**

### 2. Suffix Array (SA)

![](https://imgur.com/pYDBPu5.png)

Example from: https://discuss.codechef.com/t/a-tutorial-on-suffix-arrays/2950

`sa` is implemented using list in python. Each index points to ith order kmer in the whole reference.

> \[indecies of ordered kmers alphabtically\]

To find a pattern in `sa` , binary search is performed using these indecies since the kmers are ordered. the pattern is matched each time against the kmer selected by binary seach untill it reaches a match. If the pattern fails to reach a match it returns **-1**, else, **[ID, pos]**

`sa` is constructed from _m_ genome in logarithmic time **O(|_m.log(m)_|)** and each pattern _n_ is found in logarithmic time **O(|_m_|.log(|_m_|))** , however, it's stored in much less memory size than `trie`

### 3. Burrow Wheeler Transform (BWT)

![](https://imgur.com/ISi1vjt.png)

Example from: Zhang, D., Liu, Q., Wu, Y., Li, Y., & Xiao, L. (2013). Compression and Indexing Based on BWT: A Survey. _2013 10Th Web Information System And Application Conference_. doi: 10.1109/wisa.2013.20\

`bwt` is implemented using list and dictionary in python. Each index points to a suffix in the whole reference.

> {index: 'nucleotide', index: 'nucleotide', ..., index: '$', ..., index: 'nucleotide'}

along with `last2first` list to point to this suffix in a column of ordered suffixes, which necessary to search for pattern through going back and forth from BWT to the first column.
![](https://i.imgur.com/P1SnN3e.png)

Example from: Rocha, M., & Ferreira, P. Bioinformatics Algorithms (p. 357)\

To find a pattern in `bwt` , back and forth walk through the inverted pattern in the first and last column. the pattern is matched if it reaches its first character in the last column. If the pattern fails to reach a match it returns _-1_, else, _\[ID, pos\]_

`bwt` is constructed from _m_ genome in logarithmic time _O(|*m*|.log(|*m*|))_ and each pattern _n_ is found in linear time _O(|*n*|)_.

## Input and Output

### Input

- #### Reference genome file `-r` str()
  fasta/fastq file
- #### Sequence reads file `-s` str()
  fasta/fastq file. _paired reads are not supported_
- #### kmer size `-k` int()
  smaller kmer size means more allowance for mismatches
- #### Minimum count of matched kmers `-c`int()
  minimum allowed number of kmers matching the reference in sequence to be reported.
- #### Minimum matching percentage `-p` int()
  minimum allowed percentage of similarity between matched part of read and covered stretch of genome
- #### Batch size `-b` int()
  how many sequence reads to be loaded into memory per iteration to be mapped

### Output

- #### pseudo SAM file `-o` str()
  a file containing only read name, reference name, position, and read sequence per match

## Getting started

### Installing the package

- Download the latest release: [releases](https://github.com/anazhmetdin/Sternum/releases)
- In your command line environment:

      pip install path/to/sternum-x.x.x-py2.py3-none-any.whl

### Run an example

- In your Command Line environment:

      sternum -m method -r path/to/reference.fastx -s path/to/sequence.fastx -k kmerSize -p minPercentage -c minKcount -b batchSize -o path/to/myfirstmap

- this file will be genrated:
  path/to/myfirstmap*\$m*\$sequenceID.sam
- you can try with files in [sternum/data](https://github.com/anazhmetdin/Sternum/tree/master/data)
