import os, sys, argparse
parser=argparse.ArgumentParser()
parser.add_argument('input',  help='Input file location')
parser.add_argument('-o', '--output', help='Output file location')
args=parser.parse_args()
if not os.path.isfile(args.input):
	sys.exit('ERROR: File '+args.input+' is not a valid file')
f_input=os.path.abspath(args.input)
name_input=os.path.basename(f_input)
if args.output :
	f_output=os.path.abspath(args.output)
else:
	f_output=os.path.abspath('.'.join(name_input.split('.')[:-1])+'.nif') if '.' in name_input else f_input+'.nif'

class Nif:
	info_list=[]
	def __init__(self, record):
		middle1=record.strip().split('\t')
		middle2=middle1[0].split('_')
		middle3=middle1[9].split('"')[1].split('_')
		self.chrname=middle2[1]
		self.info_list.append(self.chrname)
		self.start=int(middle2[2])+int(middle1[3])
		self.info_list.append(self.start)
		self.stop=int(middle2[2])+int(middle1[4])
		self.info_list.append(self.stop)
		self.score=middle1[5]
		self.info_list.append(self.score)
		self.ens_id=middle2[0]
		self.info_list.append(self.ens_id)
		self.M_chrname=middle3[1]
		self.info_list.append(self.M_chrname)
		self.M_start=int(middle3[2])+int(middle1[10].split()[1][:-1])
		self.info_list.append(self.M_start)
		self.M_stop=int(middle3[2])+int(middle1[11].split()[1][:-1])
		self.info_list.append(self.M_stop)
		self.M_ens_id=middle3[0]
		self.info_list.append(self.M_ens_id)
def Main(infile,outfile):
	table=[]
	file=open(infile,'r')
	file_write=open(outfile,'w')
	i=1
	for line in file:
		while i<100000:
			i+=1
			if line:
				nif=Nif(line)
				table.append(nif.info_list)
				del(nif)
		else: 
			i=1
			for records in table:
				file_write.write('\t'.join(str(records)))
			table=[]
	
if __name__=='__main__':
	Main(f_input,f_output)



