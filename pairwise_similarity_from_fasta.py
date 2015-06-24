#### Build a similarity matrix from a given fastq file,
#### using pairwise2 module in Biopython, in order to group the sequences
#### into clusters. Each fastq file is only compared with one
#### another at a time. Only suitable for small sequences.
#!/usr/bin/python

import os, sys, argparse, itertools
import numpy as np
from Bio import pairwise2, SeqIO
parser=argparse.ArgumentParser()
parser.add_argument('input_fastq',metavar='input_fastq', help='Input the fastq read file')
args=parser.parse_args()

#### read the fastq file into a python list
def fastq_to_list(file):
	fastqfile=open(file,'rU')
	return list(SeqIO.parse(fastqfile,'fasta'))

#### perform pair-wise similarity calculation and build the similarity matrix
def seq_handshake(seqio_list):
	seq_names=[]
	sml_matrix=np.zeros(shape=(len(seqio_list), len(seqio_list)))
	for i in range(len(seqio_list)):
		seq_names.append(seqio_list[i].id)
		for k in range(i+1, len(seqio_list)):
			effective_length=min(len(seqio_list[i]),len(seqio_list[k]))
			#### 2 points for perfect match, -1 for mismatch, -3 for gap opening, -1 for gap extension.
			#### only_one_alignment and score_only spped up the calculation dramatically
			#### gaps at the end of both sequences are not penalized to cope with large spam of length
			sml_matrix[i,k]=pairwise2.align.globalms(seqio_list[i].seq,seqio_list[k].seq,2,-1,-3,-1,one_alignment_only=1,score_only=1,
			penalize_end_gaps=0)/float(effective_length)
	return sml_matrix, seq_names

####
similarity_matrix,seqname_list=seq_handshake(fastq_to_list(args.input_fastq))
f=open('matrix.csv','w')
f.write(','.join(seqname_list)+'\n')
np.savetxt(f,similarity_matrix,delimiter=',')
f.close()
