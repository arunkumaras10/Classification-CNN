import string
import os
from os import listdir
from os.path import isfile, join

limit=1899

import sys

pb=str(sys.argv[1])

mypath="./Renamed"+pb+"/"
dirs=os.listdir(mypath)
if not os.path.exists("./Filtered"+pb+"/"):
	os.makedirs("./Filtered"+pb+"/")
onlyfiles = os.listdir(mypath)
for fname in onlyfiles:
	buf=''
	cc=0	 	
	with open(mypath+'/'+fname, "r") as f:
		for c in f.read():
		 	buf+=c
		 	cc+=1
		 	#print fname +" "+str(cc)
	if cc<limit:
		newfile=open('./Filtered'+pb+'/'+fname,'w')
		newfile.write(buf)
		newfile.close()