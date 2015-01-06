import itertools
import os

############################################################
#def write_file(
barcode_dict=[]
duplicate=[]
barcode=[]
with open('/fs/lustre/wrk/shni/files/case_control.txt','r') as file:

	for line in itertools.islice(file,1,None):
		barcode.append(line.split())
		identity=line.split()[:2]
		if identity in barcode_dict:
			duplicate.append(identity)
			barcode_dict.append(identity)
		else:
			barcode_dict.append(identity)
##################
	duplist=[]
	for index, val in enumerate(barcode_dict):
		if val in duplicate:
			duplist.append(index)	 
	duplist=sorted(duplist,reverse=True)

	for index in duplist:
		del barcode[index]
	file.close()
##############################################################################################
for lines in barcode:
	globals()[lines[0]+lines[1]]=[]
obsolete=[]
#############################################################################################
#with open('/fs/lustre/wrk/shni/py_code/test.fastq', 'r') as testfile:
with open('/fs/lustre/wrk/shni/files/8q24/8q24_19', 'r') as testfile:
	while True:
		code=list(itertools.islice(testfile,4))
		if code == []:
			print 'file is over'
			break
		string=code[1][:5]
		found = 0
		code=code[0]+code[1][6:]+code[2]+code[3][6:]
		for lines in barcode:
			if string in lines[2:]:
				globals()[lines[0]+lines[1]].append(code)	
				found = 1
				break

		if found == 0:
			obsolete.append(code)
	testfile.close()			
###############################################################################
with open('/fs/lustre/wrk/shni/files/8q24/obsolete.fastq','a+') as file:
		
	for items in obsolete:
		file.write(''.join(items))
	file.close()
for lines in barcode:
	with open ('/fs/lustre/wrk/shni/files/8q24/%s/%s%s' %(lines[0],lines[0],lines[1]) ,'a+') as finalfile:
		string=globals()[lines[0]+lines[1]]
		for items in string:
			finalfile.write(''.join(items))
		finalfile.close()
