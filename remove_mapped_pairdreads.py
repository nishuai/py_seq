#### Removes reads from host for a better performance of virus genome denovo assembly
#### Input: sam file from Tophat or other mapping softwear, paired end fastq files 1 and 2
#### Once reads found to be mapped to the host genome then delete the both reads in 2 paired end files
#!/usr/bin/python
import os, sys, argparse, itertools, numpy
parser=argparse.ArgumentParser()
parser.add_argument('input_read1',metavar='read1', help='Input the first paired end fastq read file')
parser.add_argument('input_read2',metavar='read2', help='Input the second paired end fastq read file')
parser.add_argument('input_sam',  help='Input the mapped sam file')
parser.add_argument('-o','--outputdir', default='.',help='Specify the output directory or output to the current directory') 
args=parser.parse_args()
if not os.path.isfile(args.input_read1): 
	sys.exit('ERROR: File '+args.input_read1+' is not a valid read1 file')
if not os.path.isfile(args.input_read2): 
	sys.exit('ERROR: File '+args.input_read2+' is not a valid read2  file')
if not os.path.isfile(args.input_sam):
	sys.exit('ERROR: File '+args.input_sam+' is not a valid sam file')

#### check the intergrity of the two fastq files, store the seq-names in the meantime
#### make sure they have identical seq-names (qname in sam file)
def get_reads_seqnames(file1, file2):
	reads1=[]
	reads2=[]
	read_seqnames=[]
	
	print 'Starting intergrity check of two input read files...'
	read1=open(file1)
	read2=open(file2)
	while True:
		code1 = list(itertools.islice(read1,4))
		code2 = list(itertools.islice(read2,4))
		if code1 == [] and code2 == []:
			print 'Intergrity check completed, the two read files are of the same origin.'
			break
		if code1[0].split()[0]==code2[0].split()[0]:
			reads1.append(code1)
			reads2.append(code2)
			read_seqnames.append(code1[0].split()[0][1:])	
		else: 
			sys.exit('ERROR: Two input fastq files are not in correspondence, read names do not match.')
	print 'Total number of reads: '+str(len(reads1))
	read1.close()
	read2.close()
	return reads1,reads2,read_seqnames
#### read the sam file extract the seq_names from the sam file
def get_SAM_seqnames(samfile):
	print 'Start reading the SAM file...'
	sam_seqnames=[]
	sam_file=open(samfile)
	number_records=0
	while True:
		code=list(itertools.islice(sam_file,1))
		if code == []:
			print 'SAM file reading completed, '+str(number_records)+' reads mapped to the genome.'
			break
		if code [0][0] != '@' and int(code[0].split()[3]) != 0: 
			sam_seqnames.append(code[0].split()[0])
			number_records+=1
	sam_file.close()
	return sam_seqnames
#### sort the seqnames from both read file and sam file
#### in order to ease downstream comparison
def sort_sam_seqnames(seqnames):
	print 'Start sorting sam seqnames...'
	seqnames=set(seqnames)
	return sorted(seqnames)

#### sort two reads files according to their seqnames
def sort_reads(readslist1,readslist2,read_seqnames):
	print 'Start sorting read seqnames...'
	read_seqnames=numpy.array(read_seqnames)
	#### sort the reads according to their names
	index=read_seqnames.argsort()
	readslist1=numpy.array(readslist1)
	readslist2=numpy.array(readslist2)
	readslist1=readslist1[index]
	readslist2=readslist2[index]
	readslist1=readslist1.tolist()
	readslist2=readslist2.tolist()
	read_seqnames=read_seqnames[index]
	read_seqnames=read_seqnames.tolist()
	print 'Sorting reads and read seqnames completed'
	return readslist1,readslist2,read_seqnames

#### write the list file (fastq files with mapped reads deleted)
def write_fastq_list(listname,path):
	with open(path+'/'+listname+'mapped_removed.fastq', 'a+') as file:
		for sublist in globals()[listname]:
			for lines in sublist:
				file.write(lines)
	file.close()
#### Main function: delete the mapped reads from the two read files according to the SAM file

new_reads1=[]; new_reads2=[];
def Main(readfile1,readfile2,samfile):
	reads1,reads2,reads_seqnames=get_reads_seqnames(readfile1,readfile2)
	SAM_seqnames=get_SAM_seqnames(samfile)	
	SAM_seqnames=sort_sam_seqnames(SAM_seqnames)
	#### must not sort the seqnames before sorting the reads
	reads1,reads2,reads_seqnames=sort_reads(reads1,reads2,reads_seqnames)
	#### always compare with the first element in seqnames in SAM file,
	#### if match is found, delete the first element in SAM seqnames,
	#### Therefore a dummy element has to be added to the end of SAM seqnames,
	#### to avoid SAM_sequence to be empty and index out of range.
	SAM_seqnames.append('DUMMY')
	for i in range(len(reads_seqnames)):
		if reads_seqnames[i] == SAM_seqnames[0]:
			new_reads1.append(reads1[i]); new_reads2.append(reads2[i]);
			del SAM_seqnames[0] 
	#### quote the variable name to enable concatenation with path to make filename
	#### variable itself are found using globals()[variable_name])
	write_fastq_list('new_reads1', args.outputdir); write_fastq_list('new_reads2',args.outputdir)		

if __name__=='__main__':
	Main(args.input_read1,args.input_read2,args.input_sam)
