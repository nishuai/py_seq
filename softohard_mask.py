### this script makes softmasked genome into hardmasked genome
### simply by converting all lower case letter into 'N'
import os

path_file='/wrk/shni/eel/genomes/hg38_iupac_masked.fa'
path_file2='/wrk/shni/eel/genomes/test.fa'

def maskline(string):
	if string.islower():
		return 'N'*(len(string)-1)+'\n'
	elif string.isupper():
		return string
	else:
		result=[]
		for char in string:
			result.append(char if char.isupper() else 'N')
		return ''.join(result[:-1])+'\n'



file = open(path_file, 'r')
masked_file=open(file.name.split('.')[0]+'_masked.'+file.name.split('.')[1],'w')

for lines in file:
	if lines.startswith('>'):
		print 'now starts processing %s' %lines[1:]
		masked_file.write(lines)
	else:
		masked_file.write(maskline(lines))
file.close()
masked_file.close()

