import string
import os
from os import listdir
from os.path import isfile, join
import commands


inputFile='cleanedtemp'
outputFile='renamedtemp'
print commands.getoutput("./variableRenamer "+inputFile+" "+outputFile);