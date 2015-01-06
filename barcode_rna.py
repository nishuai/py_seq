import itertools
import os
file_loci='/fs/lustre/wrk/shni/files/rna-seq-wei/test/'
######################## Create the search table ############################################

table=[['vcap_rfx6.5','vcap_rfx6.6','vcap_hoxb13.6','vcapneg','lncap_hoxb13.6','lncapneg','22rv1hoxb13.6','22rv1neg'],['TAAT','ATTT','TCGAT','AGCCT','TTCT','AAGT','GGAAT','CCTCT']]
######################## INITIALIZE LISTS################################################### #############################################################################################
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
##########################
os.chdir(file_loci)
initiate_list()
for fastq in os.listdir(file_loci):
	if os.path.isfile(file_loci+fastq):
		with open (fastq) as input:
			while True:
				code = list(itertools.islice(input,4))
				if code == []:
					print 'file is over'
					break
				found = 0
				for lines in table[1]:
					if code[1].startswith(lines):
						found = 1
						trim=len(lines)
						code=[code[0],code[1][trim:],code[2],code[3][trim:]]
						globals()[lines].append(code)
						break
			
				if found == 0:
					obsolete.append(code)
##### Obsolete contails the original barcode in order to ckeck later

			print 'file %s is successfully processed, now start to write the files' % fastq
			check_creat_path(file_loci+'classified/')
			new_table=table[1][:]
			new_table.append('obsolete')
			for listnames in new_table:
				write_list(listnames, file_loci+'classified')
			initiate_list()
			input.close()
####################### Rename file according to treatment
for files in os.listdir(file_loci+'classified/'):
	print files; print table[1];
	if str(files)[:-6] in table[1]:
		os.rename(file_loci+'classified/'+files,file_loci+'classified/'+table[0][table[1].index(str(files)[:-6])]+'.fastq')
#
