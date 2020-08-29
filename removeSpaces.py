import re
import string
import os
from os import listdir
from os.path import isfile, join
import commands

chars =''
with open('temp',"r") as f:
	for c in f.read():
		chars=chars+c

#print chars
chars=re.sub('# *include *.*','',chars)
chars=re.sub(' +',' ',chars)
chars=re.sub('[\t]+','',chars)
chars=re.sub('[\n][\n]+','\n',chars)

tf=open('clean.cpp','w')
tf.write(chars)
tf.close()
chars = commands.getoutput(" g++ -E clean.cpp")
os.remove('clean.cpp')
chars=re.sub('# *.*','\n',chars)

chars=re.sub(' +',' ',chars)
chars=re.sub('[\t]+','',chars)
chars=re.sub('[\n][\n]+','\n',chars)

with open("cleanedtemp", "w") as text_file:
	text_file.write(chars)