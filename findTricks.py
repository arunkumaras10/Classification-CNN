import operator
import re
import string
import os
from os import listdir
from os.path import isfile, join
import commands
import urllib
import sys

no_sol=100
class_no=1
idx=0

tricks=['stack','queue','map','priority_queue','set','unordered_set','pair','sort','long long']
regexp={}
count={}

for i in tricks:
	exp=i+' *<.*>'
	# print exp
	regexp[i]=re.compile(exp)
	count[i]=0.0

regexp['long long']=re.compile('long long')
regexp['sort']=re.compile('sort.*(.*)')

# string="int main(){ char h[1000009];std::stack<int>s;int D[1000009];}"
# print 'checking for stack in '+string
# if regexp['stack'].search(string):
# 	print 'found'
# else:
# 	print 'not found'


# print("Enter the problem id : ")
prob_name=str(sys.argv[1])

if not os.path.exists("data"+prob_name):

	#processing the problem id
	r = re.compile("([0-9]+)([a-zA-Z]+)")
	m = r.match(prob_name)
	problem = m.group(1)
	section = m.group(2)

	#configuring url for getting the submission ids
	SUBMISSION_URL1 = 'http://codeforces.com/problemset/status/{prob}/problem/{sec}/page/{no}?order=BY_PROGRAM_LENGTH_DESC'
	SOURCE_CODE_BEGIN1 = 'var viewableSubmissionIds = ['

	#initialising
	submission=[]
	i=1

	#parsing the submission status(html)
	while True:
		submission_info = urllib.urlopen(SUBMISSION_URL1.format(prob=problem,sec=section,no=i)).read()
		start_pos = submission_info.find(SOURCE_CODE_BEGIN1) + len(SOURCE_CODE_BEGIN1)
		end_pos = submission_info.find("];", start_pos)
		result = submission_info[start_pos:end_pos].replace("\"","").replace("\r","").replace("\n","").replace(" ","")
		arr=result.split(",")
		i=i+1
		if arr[0] in submission:
			break
		submission.extend(arr)
		if i > 4:
			break

	print("collected submission ids")
	print(len(submission))
	#print(submission)

	#phase 2 : retrieving the code for each submission id
	MAGIC_START_POINT = 17000
	#configuring the url for getting code
	SOURCE_CODE_BEGIN2 = '<pre class="prettyprint lang-cpp program-source" style="padding: 0.5em;">'
	SUBMISSION_URL2 = 'http://codeforces.com/contest/{prob}/submission/{sub_no}'

	#initialising symbols to be replaced
	replacer = {'&quot;': '\"', '&gt;': '>', '&lt;': '<', '&amp;': '&', "&apos;": "'","&#39;":"'"}
	keys = replacer.keys()

	#parsing symbols
	def parse(source_code):
	    for key in keys:
	        source_code = source_code.replace(key, replacer[key])
	    return source_code

	#creating a directory for the problem
	if not os.path.exists("data"+prob_name):
		os.makedirs("data"+prob_name)

	ctr = 0;
	#parsing the html code and creating a file for each submission
	for j in submission:
		# print("hello ")
		# print(j)
		submission_info = urllib.urlopen(SUBMISSION_URL2.format(prob=problem,sub_no=j)).read()
		start_pos = submission_info.find(SOURCE_CODE_BEGIN2) 
		if start_pos == -1 :
			continue
		start_pos += len(SOURCE_CODE_BEGIN2)
		end_pos = submission_info.find("</pre>", start_pos)
		result = parse(submission_info[start_pos:end_pos]).replace('\r', '')

		file=open("data" + '/'+j,"w")
		file.write(result)
		file.close()
			

		ctr+=1
		if ctr >= no_sol :
			break
		
	print("Successfully scrapped solutions: ",ctr)
#Pre-processing Begins
os.system("python removeSpaces.py "+prob_name)

# print 'Preprocessing done'

mypath="./Clean-B"+prob_name+"/"
if not os.path.exists(mypath):
	print mypath+" not found"
onlyfiles = os.listdir(mypath)
fc=0
for fname in onlyfiles:
	chars =''
	with open(mypath+fname, "r") as f:
		for c in f.read():
			chars=chars+c

	for i in tricks:
		if regexp[i].search(chars):
			count[i]+=1
			# print i+' found in '+fname
	fc+=1
# print count
# print fc
for i in tricks:
	count[i]/=fc

count = sorted(count.items(), key=operator.itemgetter(1))
#print(count)
#print("Begins")
print("Try using : "+str(count[len(count)-1][0]))
# print(type(count[0][1]))
# if count[len(count)-1-i] <= float(0.5):
# 	print(count[len(count)-1-i])
# else:
# 	for i in range(len(count)):
# 		if count[len(count)-1-i] >= float(0.5):
# 			 print(count[len(count)-1-i])

