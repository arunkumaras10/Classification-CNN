import string
import os
from os import listdir
from os.path import isfile, join
import sys

pb=str(sys.argv[1])

d = {}
for i in range(32,127):
	d[chr(i)] = i-31

limit=1899

mypath='./Filtered'+pb+'/'
onlyfiles = os.listdir(mypath)
if not os.path.exists("./Final"+pb+"/"):
	os.makedirs("./Final"+pb+"/")
for fname in onlyfiles:		
	with open('./Filtered'+pb+'/'+fname, "r") as f:
		x = open('./Final'+pb+'/'+fname, "w")
		l=0	
		for c in f.read():
			if c != '\n' and c != '\t' and ord(c) < 128:
				x.write('%d' % d[c])
				l=l+1
				x.write(" ")
		#print l
		while l<=limit:
			x.write('0 ')
			l+=1			
		x.close()