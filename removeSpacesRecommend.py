import re
import string
import os
from os import listdir
from os.path import isfile, join
import commands
import sys

pb=str(sys.argv[1])

mypath='./data'+pb+'/'
onlyfiles = os.listdir(mypath)
if not os.path.exists("./Clean-B"+pb+"/"):
	os.makedirs("./Clean-B"+pb+"/")
for fname in onlyfiles:
	chars =''
	with open(mypath+fname,"r") as f:
		for c in f.read():
			chars=chars+c

	#print chars
	chars=re.sub('# *include *.*','',chars)
	chars=re.sub(' +',' ',chars)
	chars=re.sub('[\t]+','',chars)
	chars=re.sub('[\n][\n]+','\n',chars)

	tf=open('clean'+pb+'.cpp','w')
	tf.write(chars)
	tf.close()
	chars = commands.getoutput(" g++ -E clean"+pb+".cpp")
	os.remove('clean'+pb+'.cpp')
	chars=re.sub('# *.*','\n',chars)

	chars=re.sub(' +',' ',chars)
	chars=re.sub('[\t]+','',chars)
	chars=re.sub('[\n][\n]+','\n',chars)

	with open("./Clean-B"+pb+"/"+fname, "w") as text_file:
		text_file.write(chars)