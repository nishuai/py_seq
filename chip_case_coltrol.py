import os
import csv
filepath='/home/u22/shni/files/gohong_chipseq.csv'
file=open(filepath, 'rb') 
csvfile=csv.reader(file)
data=[row for row in csvfile]

##all right till here########################################

write_file=open('chip_coltrol.csv','w')
title=','.join(['execute','macsSettingNo','expName','workingDir','chipSeqRawDataFolder','treat','control','treatDataAbbre','controlDataAbbre','organism','genomeBuildVersion','mFold_low','mFold_high','bandwidth','pValue','tagSize','genomeSize','memeChipModeCode','topNumberOptStr','flankLengthOptStr','analysisDepth','programPairing'])

write_file.write(title+'\n')
##########################################
lanelist=[1,2,3,4,5,6,6,7,7,1,2,3,4,5,6,7]

#########################################
def filepath(sampleno):
	barcode=''
	libraryid=''
	for i in range(len(data)):
		if data[i][6]!='':
			libraryid=data[i][6].lower()
			if data[i][0]==sampleno:
				barcode=data[i][5]
				break
		else:
			if data[i][0]==sampleno:
				barcode=data[i][5]
				break
	laneid=int(''.join([s for s in libraryid if s.isdigit()]))
	laneid_str=('0'+str(laneid))[-2:]
	return '/wrk/data/Gonghong/%s%s/lane%d_NoIndex_L00%d_R1_001.fastq.gz.%s.fq.gz' %(libraryid[:4],laneid_str,
	lanelist[laneid-1], lanelist[laneid-1], barcode)
#############################################
def write_row(row):

	write_raw=[0,'A','%s/%s' %(row[0],row[7]),'/wrk/data/Gonghong','wrk/data/Gonghong',filepath(row[0]),filepath(row[7]),
	row[0],row[7],'human',19,10,30,300,0.00001,'D',0,1,1000,'0_25',4,'HH']
	write=','.join(str(ele) for ele in write_raw)
	return write

print filepath('VDHOXB13')
###########################################
for row in data:
	if row[0] != ''  and  row[7] != '':
		write_file.write(write_row(row)+'\n')




write_file.close()
file.close()

