#!/usr/bin/python
#### compute Top N k-mer statistics for a given fastq file
#### Author: Ni Shuai Version: 1.0

import os, sys, argparse
from ctypes import *
#### creat a map for an easy conversion of the characters
parser=argparse.ArgumentParser()
#parser.add_argument('in',metavar='input', help='Input the fastq read file')
parser.add_argument('-k',help='K-mer length to look up with')
parser.add_argument('-top',help='The number of most frequently observed K-mers to be reported')
args=parser.parse_args()


#### check the value of k and set the according shifting distance.
k=int(args.k)

try: k+1
except ValueError:
                sys.exit('ERROR: The value of K should be an interger smaller than 16')

if k > 15: sys.exit('ERROR: Sorry, the programme only supports statistics for k-mer shorter than 16')

shift=2*(k-1)

#### set the translation maps for original string and its reverse complement.
tr={'A': 0, 'a': 0, 'c': 3, 'C': 3, 'g': 1, 'G': 1, 'T': 2, 't': 2}
rc={'A': 2, 'a': 2, 'c': 1, 'C': 1, 'g': 3, 'G': 3, 'T': 0, 't': 0}

#### initiate the hash array
h_array=(c_int*2**(2*k-1))()

sequence='AATTCGACACCGTTAGACGATTGATAGAGAGAGAGAGAAAAACCGCG'

#### calculate the hash value for the first k-mer in the sequence,
#### bases of the sequence are encoded in byte.

#### Hash value is the sum of the binary values of the original sequence and its
#### reverse complement, resulting in a identical hashing value for reverse complements.


def start_seq_bin(seq):
        bin_index=0
        rc_index=0
        for i in range(k):
                bin_index=bin_index + (tr[seq[i]] << 2*i)
                rc_index=rc_index + (rc[seq[i]] << 2*i)
        return bin_index,rc_index

#### shift the k-mer one base further to the end of the sequence, avoiding
#### uncessary encoding all bases in bytes again.

def read_one_bin(bin_number,chr,map):
        return (bin_number>>2) |  map[chr] << shift

#### go through the entire sequence and record the apperence.
#### Note: In order to save computing time during masking, the frequencies of the reversed sequences are
#### calculated instead of the sequences themselve. A simple reverse is added to the final result.

def calc_seq_index(seq):
        bin_index, rc_index = start_seq_bin(seq)
        smaller_bin=min(bin_index,rc_index)
        h_array[smaller_bin]=h_array[smaller_bin]+1
        for i in seq[k:]:
                bin_index=read_one_bin(bin_index,i,tr)
                rc_index=read_one_bin(rc_index,i,rc)
                smaller_bin=min(bin_index,rc_index)
                print smaller_bin
                h_array[smaller_bin]=h_array[smaller_bin]+1

