import string
import sys
import os
from os import listdir
from os.path import isfile, join

limit=1899

buf=''
cc=0	 	
with open('renamedtemp', "r") as f:
	for c in f.read():
	 	buf+=c
	 	cc+=1
	 	#print fname +" "+str(cc)
if cc<limit:
	newfile=open('filteredtemp','w')
	newfile.write(buf)
	newfile.close()
else:
	print 'Cannot predict tag since the solution is too long'
