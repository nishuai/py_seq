#!/usr/bin/python
# coding=utf-8
import os
import operator
import os.path
import sys
#####　file path and initiate the coorediates for two genomes
#####  'sequences' is the file contail bed file pairs of ortholog genes between mouse and human

file_path='/wrk/shni/eel/test/'
coordinate_file1='gene_coor.tsv'
coordinate_file2='testorth_coor.tsv'


if not os.path.exists(file_path+'sequences'):
	os.makedirs(file_path+'sequences')

hg38_length=['chr1    248956422', 'chr2    242193529', 'chr3    198295559', 'chr4    190214555', 'chr5    181538259', 'chr6    170805979', 'chr7    159345973', 'chr8    145138636', 'chr9    138394717', 'chr10   133797422', 'chr11   135086622', 'chr12   133275309', 'chr13   114364328', 'chr14   107043718', 'chr15   101991189', 'chr16   90338345', 'chr17   83257441', 'chr18   80373285', 'chr19   58617616', 'chr20   64444167', 'chr21   46709983', 'chr22   50818468', 'chrX    156040895', 'chrY    57227415']

mm10_length=['chr1	195471971', 'Chr2	182113224', 'Chr3	160039680', 'Chr4	156508116', 'Chr5	151834684', 'Chr6	149736546', 'Chr7	145441459', 'Chr8	129401213', 'Chr9	124595110', 'Chr10	130694993', 'Chr11	122082543', 'Chr12	120129022', 'Chr13	120421639', 'Chr14	124902244', 'Chr15	104043685', 'Chr16	98207768', 'Chr17	94987271', 'Chr18	90702639', 'Chr19	61431566', 'ChrX	171031299', 'ChrY	91744698']

#####  functions to manipulate strings


def writefile(path,stuff):
		file=open(path,'w')
		file.write(stuff)
		file.close()

def h_length_limit(chromosome):
	if chromosome == 'X':
		return int(hg38_length[22].split()[1])
	if chromosome == 'Y':
		return int(hg38_length[23].split()[1])
	else:
		return int(hg38_length[int(chromosome)-1].split()[1])

def m_length_limit(chromosome):
	if chromosome.strip() == 'X':
		return int(mm10_length[19].split()[1])
	if chromosome.strip() == 'Y':
		return int(mm10_length[20].split()[1])
	else:
		return int(mm10_length[int(chromosome)-1].split()[1])

def liftup(length_limit,coordinate,value):
	lifted=int(coordinate)+value
	return str(lifted) if lifted < length_limit else str(length_limit)

with open(file_path+coordinate_file1) as file:
	file.readline()
	i = 1
	for line in file:
		line=line.split('\t')
		if len(line[3]) < 3 and len(line[7].strip()) < 3:
			h_len_lim=h_length_limit(line[3])
			m_len_lim=m_length_limit(line[7])
			content1='chr'+line[3]+'\t'+(str(int(line[1])-500000) if int(line[1]) > 500000 else str(0))+'\t'+liftup(h_len_lim,line[2],500000)+'\t'+line[0]+'_'+'chr'+line[3]+'_'+(str(int(line[1])-500000) if int(line[1]) > 500000 else str(0))+'_'+liftup(h_len_lim,line[2],500000)+'\t'
			content2='chr'+line[7].strip()+'\t'+(str(int(line[5])-500000) if int(line[5]) > 500000 else str(0))+'\t'+liftup(m_len_lim,line[6],500000)+'\t'+line[4]+'_'+'chr'+line[7].strip()+'_'+(str(int(line[5])-500000) if int(line[5]) > 500000 else str(0))+'_'+liftup(m_len_lim,line[6],500000)+'\t'
			os.makedirs(file_path+'sequences/'+str(i)+'thpair')
			writefile(file_path+'sequences/'+str(i)+'thpair/'+line[0]+'.bed',content1)
			writefile(file_path+'sequences/'+str(i)+'thpair/'+line[4]+'.bed',content2)
			i += 1
file.close()


