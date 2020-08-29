import string
import os
from os import listdir
from os.path import isfile, join

d = {}
for i in range(32,127):
	d[chr(i)] = i-31

limit=1899

with open('filteredtemp', "r") as f:
	x = open('finaltemp', "w")
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

	print 'mapping done'