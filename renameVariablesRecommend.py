import string
import os
from os import listdir
from os.path import isfile, join
import commands

import sys

pb=str(sys.argv[1])

mypath="./Clean-B"+pb+"/"
if not os.path.exists(mypath):
	print mypath+" not found"
dirs=os.listdir(mypath)
if not os.path.exists("./Renamed"+pb+"/"):
	os.makedirs("./Renamed"+pb+"/")
onlyfiles = os.listdir(mypath)
for fname in onlyfiles:
	inputFile=mypath+fname
	outputFile="./Renamed"+pb+"/"+fname
	print commands.getoutput("./variableRenamer "+inputFile+" "+outputFile);
