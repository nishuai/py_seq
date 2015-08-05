#### Find the most frequently aligned target genome from a aligner like Bowtie or blast output
#### Input: Alignment sam file or a local blast result in csv or tsv format
#### 30.07.2015

#!/usr/bin/python
import os, sys, argparse, re
from itertools import islice

#### passing arguments
parser=argparse.ArgumentParser()
parser.add_argument('input', help='Input file in sam or a xsv format from blast output')
parser.add_argument('-top', default=10,  help='The number of most aligned genomes reported by the programme, default is 10')
parser.add_argument('-o','--outputdir', default='.',help='The output directory or output to the current directory') 
args=parser.parse_args()


try:int(args.top)+1
except ValueError:
		sys.exit('ERROR: top should be an integer')
topn=int(args.top)
print 'the default of top is: ' + str(topn)
if not os.path.isfile(args.input): 
	sys.exit('ERROR: File '+args.input+' is not a valid file')

#### determine the format of the input file
def filetype_check(file):
	sam_header=0
	csv=0
	tsv=0
	hmm=0
	f_test=open(file,'r')
	head10=list(islice(f_test,10))
	for i in range(10):
		if re.match('^@[A-Z][A-Z]\t[A-Z][A-Z]', head10[i]) and len(head10[i].split('\t'))<4:
			sam_header+=1
		elif max(len(re.split(r'\s{2,}',head10[i])),len(head10[i].split('\t')))<len(head10[i].split(',')):
			csv+=1
		elif len(re.split(r'\s{2,}',head10[i]))<len(head10[i].split('\t')):
			tsv+=1
		elif re.match('^#',head10[i]) or len(re.split(r'\s{2,}',head10[i]))>len(head10[i].split('\t')):
			hmm+=1
		
	if sam_header>0:
		while True:
			record=list(islice(f_test,1))
			if record==[]:
				sys.exit('ERROR: the format of the input is neither SAM nor xsv, please check the input')
			if len(record[0].split('\t'))>10 and record[0].split('\t')[1].isdigit():
				f_test.close()
				return 'sam',record[0]
	elif csv==10:
		f_test.close()
		return 'csv',head10[9]
	elif tsv>8:
		f_test.close()
		return 'tsv',head10[9]
	elif hmm>8:
		f_test.close()
		return 'hmm',head10[9]
	else:
		sys.exit('ERROR: the format of the input file is neither SAM nor xsv, please check the input')

#### find the column(s) where the informatin of the species should be extracted

def tax_column(file):
	gi_column=None; name_column=None
	gi_match=0; name_match=0
	sep=None
	filetype, example_line=filetype_check(file)

	if filetype =='csv':
		sep=','
	elif filetype=='tsv':
		sep='\t'
	
	if filetype in ['csv']:
		for i in range(len(example_line.split(sep))):
			if re.match('gi.[0-9]*\|',example_line.split(sep)[i]):
				gi_match+=1
				gi_column=i
			if len(example_line.split(sep)[i].split())> 1 and 'complete' not in example_line.split(sep)[i]:
				name_match+=1
				name_column=i
		if gi_match==1 and name_match==1:
			return filetype, gi_column+1, name_column+1
		else:
			sys.exit('ERROR: no taxonomic information found in the data, please check the input')
	elif filetype in ['tsv']:
		for i in range(len(example_line.split(sep))):
			if re.match('gi.[0-9]*\|',example_line.split(sep)[i]):
				gi_match+=1
				gi_column=i
			if len(example_line.split(sep)[i].split())> 1 and 'complete' not in example_line.split(sep)[i]:
				name_match+=1
				name_column=i
		if gi_match==1 and name_match==1:
			return filetype, gi_column+1, name_column+1
		else:
			sys.exit('ERROR: no taxonomic information found in the data, please check the input')
	elif filetype in ['hmm']:
		for i in range(len(re.split(r'\s{2,}',example_line))):
			if re.match('gi.[0-9]*\|',re.split(r'\s{2,}',example_line)[i]):
				gi_match+=1
				gi_column=i
			if len(re.split(r'\s{2,}',example_line)[i].split())> 3:
				name_match+=1
				name_column=i
		if gi_match==1 and name_match==1:
			return filetype, gi_column+1, name_column+1
		else:
			sys.exit('ERROR: no taxonomic information found in the data, please check the input')
	elif filetype == 'sam':
		if re.match('gi.[0-9]*\|', example_line.split(sep)[2]):
			return filetype, 3, None
		else:  sys.exit('ERROR: the 3rd column does not contain the taxonomic information in the sam file, please check the input')
#### defining methods for line operation
class Csv_hit:
	def __init__(self,record,gi_column, name_column):
		self.words=record.split(',')
		self.gi_number=self.words[gi_column-1].split('|')[1]
		self.names=self.words[name_column-1].split()

class Tsv_hit:
	def __init__(self,record,gi_column, name_column):
		self.words=record.split('\t')
		self.gi_number=self.words[gi_column-1].split('|')[1]
		self.names=self.words[name_column-1].split()

class Sam_hit:
	def __init__(self,record,gi_column):
		self.words=record.split('\t')
		if record [0] != '@' and int(record.split()[3]) != 0: 
			self.gi_number=record.split('\t')[gi_column-1].split('|')[1]
		else:
			self.gi_number=None

class Hmm_hit:
	def __init__(self,record,gi_column,name_column):
		self.words=re.split(r'\s{2,}',record)
		if record [0] != '#': 
			self.gi_number=self.words[gi_column-1].split('|')[1]
			self.names=self.words[-1].split()
		else:
			self.gi_number=None
			self.names=None


#### read the alignment file and put them into a dict, sort for statistics
def Main(file):
	species_names=dict(); gi_names=dict()
	file_type, gi_column, name_column=tax_column(file)
	matches=0
	if file_type == 'sam':
		samfile=open(file,'r')
		while True:
			code=list(islice(samfile,1))
			if code == []:
				print 'SAM file reading completed, in total '+str(matches)+' reads found matches.'
				break
			matches+=1
			record=Sam_hit(code[0], gi_column)
			if record.gi_number != None:
				gi_names[record.gi_number]=gi_names.get(record.gi_number,0)+1
		ff=open(''.join(args.input.split('.')[:-1])+'_summary.txt','w')
		sorted_gis=sorted(gi_names,key=gi_names.get,reverse=True)
		ff.write('In total '+str(matches)+' reads found matches.'+'\n')
		ff.write('Gene bank number of the most frequently mapped ' + str(topn)+' species'+'\n')
		for i in range(topn):
			ff.write('{0:>20} {1:>15} {2:>15}'.format(str(sorted_gis[i]),':',str(gi_names[sorted_gis[i]])+' times')+'\n')
		ff.close()
		samfile.close()

	if file_type in ['csv']:
		file=open(file,'r')
		matches=0
		while True:
			code=list(islice(file,1))
			if code == []:
				print 'csv file reading completed, in total '+str(matches)+' reads found matches.'
				break
			matches+=1
			record=Csv_hit(code[0],gi_column,name_column)
			gi_names[record.gi_number]=gi_names.get(record.gi_number,0)+1
			for strings in record.names:
				species_names[strings]=species_names.get(strings,0)+1
		ff=open(''.join(args.input.split('.')[:-1])+'_summary.txt','w')
		sorted_gis=sorted(gi_names,key=gi_names.get,reverse=True)
		ff.write('In total '+str(matches)+' reads found matches.'+'\n')
		ff.write('Gene bank number of the most frequently mapped ' + str(topn)+' species'+'\n')
		for i in range(topn):
			ff.write('{0:>20} {1:>15} {2:>15}'.format(str(sorted_gis[i]),':',str(gi_names[sorted_gis[i]])+' times')+'\n')
		ff.write('mostly appeared species names:'+'\n')
		for key in ['bv.','DNA','2','genome','chromosome','plasmid','sp.','subsp.','DSM','str.','1','ATCC']:
			species_names.pop(key, None)
		sorted_names=sorted(species_names,key=species_names.get,reverse=True)
		for i in range(topn):
			ff.write('{0:>20} {1:>15} {2:>15}'.format(sorted_names[i],':',str(species_names[sorted_names[i]])+' times')+'\n')

	if file_type in ['tsv']:
		file=open(file,'r')
		matches=0
		while True:
			code=list(islice(file,1))
			if code == []:
				print 'csv file reading completed, in total '+str(matches)+' reads found matches.'
				break
			matches+=1
			record=Tsv_hit(code[0],gi_column,name_column)
			gi_names[record.gi_number]=gi_names.get(record.gi_number,0)+1
			for strings in record.names:
				species_names[strings]=species_names.get(strings,0)+1
		ff=open(''.join(args.input.split('.')[:-1])+'_summary.txt','w')
		sorted_gis=sorted(gi_names,key=gi_names.get,reverse=True)
		ff.write('In total '+str(matches)+' reads found matches.'+'\n')
		ff.write('Gene bank number of the most frequently mapped ' + str(topn)+' species'+'\n')
		for i in range(topn):
			ff.write('{0:>20} {1:>15} {2:>15}'.format(str(sorted_gis[i]),':',str(gi_names[sorted_gis[i]])+' times')+'\n')
		ff.write('mostly appeared species names:'+'\n')
		for key in ['bv.','DNA','2','genome','chromosome','plasmid','sp.','subsp.','DSM','str.','1','ATCC']:
			species_names.pop(key, None)
		sorted_names=sorted(species_names,key=species_names.get,reverse=True)
		for i in range(topn):
			ff.write('{0:>20} {1:>15} {2:>15}'.format(sorted_names[i],':',str(species_names[sorted_names[i]])+' times')+'\n')


	if file_type in ['hmm']:
		file=open(file,'r')
		matches=0
		while True:
			code=list(islice(file,1))
			if code == []:
				print 'hmm file reading completed, in total '+str(matches)+' reads found matches.'
				break
			matches+=1
			record=Hmm_hit(code[0],gi_column,name_column)
			if record.gi_number != None:
				gi_names[record.gi_number]=gi_names.get(record.gi_number,0)+1
				for strings in record.names:
					for nocommas in strings.split(','):
						if nocommas:
							species_names[nocommas]=species_names.get(nocommas,0)+1
		ff=open(''.join(args.input.split('.')[:-1])+'_summary.txt','w')
		sorted_gis=sorted(gi_names,key=gi_names.get,reverse=True)
		ff.write('In total '+str(matches)+' reads found matches.'+'\n')
		ff.write('Gene bank number of the most frequently mapped ' + str(topn)+' species'+'\n')
		for i in range(topn):
			ff.write('{0:>20} {1:>15} {2:>15}'.format(str(sorted_gis[i]),':',str(gi_names[sorted_gis[i]])+' times')+'\n')
		ff.write('mostly appeared species names:'+'\n')
		for key in ['2715','86','7','5','isolate','Human','3','segment','genomic','virus,','dulcis','sequence','subtype','bv.','DNA','complete','phage','virus','strain','2','genome','chromosome','plasmid','sp.','subsp.','DSM','str.','1','ATCC']:
			species_names.pop(key, None)
		sorted_names=sorted(species_names,key=species_names.get,reverse=True)
		for i in range(topn):
			ff.write('{0:>20} {1:>15} {2:>15}'.format(sorted_names[i],':',str(species_names[sorted_names[i]])+' times')+'\n')


		
if __name__=='__main__':
	Main(args.input)
