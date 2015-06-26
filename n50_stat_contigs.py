#### take a contig file in fasta format as input and genreate statistics for the
#### contigs including total reads, mean length, N50 and N90.

#!/usr/bin/python

import os, sys, argparse
import numpy as np
from Bio import pairwise2, SeqIO
parser=argparse.ArgumentParser()
parser.add_argument('input_contig',metavar='input_contig', help='Input the fastq read file')
args=parser.parse_args()

#### get the lengths of all contigs
def get_reads_seqnames(contig_file):
	length_array=[]	
	read1=open(contig_file)
	seqio_items=SeqIO.parse(contig_file,'fasta')
	for fasta in seqio_items:
		length_array.append(len(fasta.seq))
	return sorted(length_array, reverse=True)

#### get details of a sorted array
if __name__=='__main__':
	sorted_array=get_reads_seqnames(args.input_contig)	
	n50_length=sum(sorted_array)*0.5
	n90_length=sum(sorted_array)*0.9
	print sorted_array
	accu_length=0
	for i in range(len(sorted_array)):
		accu_length=accu_length+sorted_array[i]
		if accu_length>n50_length:
			print sorted_array[i], accu_length
			n_50=sorted_array[i]
			for k in range(i+1,len(sorted_array)):
				accu_length=accu_length+sorted_array[k]
				if accu_length>n90_length:
					print sorted_array[k], accu_length
					n_90=sorted_array[k]
					break
			ff=open(''.join(args.input_contig.split('.')[:-1])+'_summary.txt','w')
			ff.write('Contig statistics for '+args.input_contig+':'+'\n\n')
			ff.write('{0:>15} {1:>15} {2:>15}'.format('Total reads',':',str(len(sorted_array)))+'\n')
			ff.write('{0:>15} {1:>15} {2:>15}'.format('Mean Length',':',str(sum(sorted_array)/float(len(sorted_array))))+'\n')
			ff.write('{0:>15} {1:>15} {2:>15}'.format('N50',':',str(n_50))+'\n')
			ff.write('{0:>15} {1:>15} {2:>15}'.format('N90',':',str(n_90))+'\n')
			break	

					
		
