import os
import numpy as np

path_pfms='/wrk/shni/eel/matrices/other_pfms/'
path_output='/wrk/shni/eel/matrices/'
class Pfm_trans():
	def __init__(self, filename):
		self.name=filename
	def content(self):
		matrix=open(path_pfms+self.name).read()
		result=[]
		for line in matrix.strip().split('\n'):
			result.append(int(number) for number in line.strip().split('\t'))
		return result
	def trans(self):
		result=self.content()
		return zip(*result)
	def normalize(self):
		result=self.trans()
		for j in range(len(result)):
			tmplist=list(result[j])
			for i in range(len(tmplist)):
				tmplist[i]=float(result[j][i])/sum(result[j]) if tmplist[i] != 0 else 0
			result[j]=tmplist
		return result
		
with open (path_output+'/transed_pfms.txt', 'w') as file_write:
	for files in os.listdir(path_pfms):
		pfm=Pfm_trans(files)
		file_write.write('>'+pfm.name+'\n')
		for lines in pfm.normalize():
				file_write.write('\t'.join(str(char) for char in lines)+'\n')
		file_write.write('\n')
		del(pfm)
file_write.close()
