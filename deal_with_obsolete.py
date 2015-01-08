### this chunk of code deals with sequences with no perfectly mached barcode, 
### sometimes a sequencing error happens and these barcode are not classified
### into any categories, so we recgonize the single error and make the right
### classification.


import itertools
from itertools import izip
import os
file_loci='/fs/lustre/wrk/shni/files/rna-seq-wei/data/obsolete/'
######################## Create the search table ############################################

table=[['vcap_rfx6.5','vcap_rfx6.6','vcap_hoxb13.6','vcapneg','lncap_hoxb13.6','lncapneg','22rv1hoxb13.6','22rv1neg'],['TAAT','ATTT','TCGAT','AGCCT','TTCT','AAGT','GGAAT','CCTCT']]

### the distance is slightly different from either hamming distance or levenstein
### distance, here we assume there is no insertion and deletions in sequencing technology.
### prefer calling it match distance.
def match_dist(str1,str2):
	## we assume str1 is always longer than str2
	len_dist=len(str1)-len(str2)
	if len_dist==0:
		return(sum(str1 != str2 for str1,str2 in izip(str1,str2)))
	if len_dist!=0:
		str1=str1[:-len_dist]
		return(sum(str1 != str2 for str1,str2 in izip(str1,str2)))

def initiate_list():
	for lines in table[1]:
		globals()[lines]=[]
	globals()['obsolete']=[]
	print 'lists are initiated'
################# Define functions 
def check_creat_path(path):
	if not os.path.exists(os.path.dirname(path)):
		print 'not exist'
		os.makedirs(os.path.dirname(path))
	else:
		print '%s alrady exist' %path
def write_list(listname,path):	
		with open(path+'/'+listname+'.fastq', 'a+') as file:
			for sublist in globals()[listname]:
				for lines in sublist:
					file.write(lines)
		file.close() 
#####main function

initiate_list()

os.chdir(file_loci)

for files in os.listdir(file_loci):
	if os.path.isfile(file_loci+files):
		with open (files) as input:
			while True:
				code = list(itertools.islice(input,4))
				dist_score=[]
				if code == []:
					print 'file is over'
					break
				barcode=code[1][:5]
				found = 0
				for string in table[1]:
					dist_score.append(match_dist(barcode,string))
				if dist_score.count(1) == 1:
					found = 1
					mached_string=table[1][dist_score.index(1)]
					trim=len(mached_string)
					code=[code[0],code[1][trim:],code[2],code[3][trim:]]
					globals()[mached_string].append(code)
					print dist_score
				dist_score=[]
			
				if found == 0:
					obsolete.append(code)
				
##### Obsolete contails the original barcode in order to ckeck later
	
			print 'file %s is successfully processed, now start to write the files' %input 
			check_creat_path(file_loci+'test/')
			new_table=table[1][:]
			new_table.append('obsolete')
			for listnames in new_table:
				write_list(listnames, file_loci+'test/')
			initiate_list()
			input.close()
####################### Rename file according to treatment
for files in os.listdir(file_loci+'test/'):
	print files; print table[1];
	if str(files)[:-6] in table[1]:
		os.rename(file_loci+'test/'+files,file_loci+'test/'+table[0][table[1].index(str(files)[:-6])]+'.fastq')

