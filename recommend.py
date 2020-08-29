from __future__ import print_function
import urllib
import json
import time, os
import re
import re
import string
import numpy as np
import scipy
import os
from os import listdir
from os.path import isfile, join
from numpy import array,newaxis
import random
from keras.models import model_from_json
import pickle
import operator
import sys


batch_size = 128
no_sol = 50

# print("Enter the problem id : ")
prob_name=str(sys.argv[1])


mypath='./'
if not os.path.exists("./data"+prob_name):
	

	#processing the problem id
	r = re.compile("([0-9]+)([a-zA-Z]+)")
	m = r.match(prob_name)
	problem = m.group(1)
	section = m.group(2)

	#configuring url for getting the submission ids
	SUBMISSION_URL1 = 'http://codeforces.com/problemset/status/{prob}/problem/{sec}/page/{no}'
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
	print(submission)

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
	print(prob_name)
	tt="data"+prob_name
	print(tt)
	os.makedirs(tt)


	ctr = 0;
	#parsing the html code and creating a file for each submission
	for j in submission:
		print(j)
		submission_info = urllib.urlopen(SUBMISSION_URL2.format(prob=problem,sub_no=j)).read()
		start_pos = submission_info.find(SOURCE_CODE_BEGIN2) 
		if start_pos == -1 :
			continue
		start_pos += len(SOURCE_CODE_BEGIN2)
		end_pos = submission_info.find("</pre>", start_pos)
		result = parse(submission_info[start_pos:end_pos]).replace('\r', '')
		file=open("data"+prob_name + '/'+j,"w")
		file.write(result)
		file.close()
		ctr+=1
		if ctr > no_sol :
			break
		
	print("Successfully scrapped solutions: ",ctr)

#Pre-processing Begins
os.system("python removeSpacesRecommend.py "+prob_name)
os.system("python renameVariablesRecommend.py "+prob_name)
os.system("python filterRecommend.py "+prob_name)
os.system("python mappingRecommend.py "+prob_name)
print("Pre-Processing Done")

#Vectorization
test_data=[]
x=[]
mypath='./Final'+prob_name+'/'
dirs=os.listdir(mypath)
onlyfiles = os.listdir(mypath)
for j in onlyfiles:
	f=open(mypath+j,'r')
	chars=f.readlines()
	f.close()
	temp=chars[0].split(" ")
	del temp[-1]
	temp=map(int,temp)
	#mm=len(temp)
	x.append(temp)

test_data=array(x)
test_data=test_data[:,:,newaxis]
X_test = test_data[:]
print(X_test.shape)
print("Vectorization Done")

X_test = X_test.astype('float32')
X_test /= 95
print(X_test.shape[0], 'predict samples')

#Loading Model
json_file = open('model.json','r')
loaded_model_json = json_file.read()
json_file.close
model = model_from_json(loaded_model_json)
model.load_weights("model.h5")
model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
print("Loaded model...")

#Predictions
classes = model.predict_classes(X_test, batch_size=batch_size, verbose=1)
print(classes)
probs = model.predict_proba(X_test, batch_size=batch_size, verbose=1)
print(probs)

mean_prob = probs.mean(axis=0)
unique, counts = np.unique(classes, return_counts=True)
v = np.argmax(counts)
print(np.asarray((unique, counts)))
print(v)
print("PREDICTED CLASS FOR THE PROBLEM IS : ",unique[v])
print (prob_name)
print(mean_prob)


# os.system("rm -rf Clean-B"+prob_name)
os.system("rm -rf Filtered"+prob_name)
os.system("rm -rf Final"+prob_name)
os.system("rm -rf Renamed"+prob_name)
# os.system("rm -rf data"+prob_name)


with open("tags_prob.txt", "rb") as myFile:
    prob_repo = pickle.load(myFile)

dict={}

for i in prob_repo:
	ans=0
	print (prob_repo[i])
	if i != "test":
		for j in range(4):
			ans+=np.square(mean_prob[j]-prob_repo[i][j])
			print (ans)
		dict[i]=np.sqrt(ans)



print (" ")

c=0
print("Recommended Problems :")
res={}
for key, value in sorted(dict.iteritems(),key=lambda (k,v):(v,k)):
	res[c]=key
	print ("%s" %(key))
	c+=1
	if c == 3 :
		break

# print(res.values())