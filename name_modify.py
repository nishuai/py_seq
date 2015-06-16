import os
import string
import argparse
import sys

parser=argparse.ArgumentParser()
parser.add_argument('-indir','--inputdirectory',help='Input directory contains all pfm files')
args=parser.parse_args()
if not args.inputdirectory:
        input_var=raw_input('No directory specified, use current directory? Y/N: ')
        if input_var.lower() in ('yes','y'):
                file_dir=os.getcwd()
        elif input_var.lower() in ('no','n'):
                sys.exit('Exit')
        else:
                sys.exit('Exit, command not recognized')
elif not os.path.exists(args.inputdirectory):
        sys.exit('ERROR: Directory does not exit')
else:
        file_dir=os.path.abspath(args.inputdirectory)

for file in os.listdir(file_dir):
        extension=os.path.splitext(file)[1]
        filename=os.path.splitext(file)[0]
        if extension=='.pfm' and len(filename.split('_'))==4:
                os.rename(file,'_'.join((filename.split('_')[3],filename.split('_')[2],filename.split('_')[0],filename.split('_')[1]))+extension)

        elif extension=='.pfm' and len(filename.split('_'))>4:
                filename=filename.replace('__','-')
                print filename
                os.rename(file,'_'.join((filename.split('_')[3],filename.split('_')[2],filename.split('_')[0],filename.split('_')[1]))+extension)

