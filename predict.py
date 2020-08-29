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

batch_size = 128

tags=["Segment Tree","Binary Search","Graph","Dynamic Programming"]

# Pre-processing Begins
os.system("python removeSpaces.py")
os.system("python renameVariables.py")
os.system("python filter.py")
os.system("python mapping.py")
# print("Pre-Processing Done")

#Vectorization
test_data=[]
x=[]
f=open('finaltemp','r')
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
# print(X_test.shape)
# print("Vectorization Done")

X_test = X_test.astype('float32')
X_test /= 95
# print(X_test.shape[0], 'predict samples')

#Loading Model
json_file = open('model.json','r')
loaded_model_json = json_file.read()
json_file.close
model = model_from_json(loaded_model_json)
model.load_weights("model.h5")
model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
# print("Loaded model...")

#Predictions
classes = model.predict_classes(X_test, batch_size=batch_size, verbose=0)
# print(classes)
probs = model.predict_proba(X_test, batch_size=batch_size, verbose=0)
# print(probs)

mean_prob = probs.mean(axis=0)
unique, counts = np.unique(classes, return_counts=True)
v = np.argmax(counts)
# print(np.asarray((unique, counts)))
# print(v)
# print("PREDICTED CLASS FOR THE PROBLEM IS : ",unique[v])
# print(mean_prob)

print(tags[unique[v]])