import re
import string
import os
from os import listdir
from os.path import isfile, join
import commands

probid="1"
ekind=["Maybe you should increment your counter variable","Maybe you should decrement your counter variable","Maybe you are not updating the counter variable","Maybe you are assigning instead of comparing"]
errors=[]
kind=[]
fname="Sol"+probid+".c"
f = open(fname, "r")
chars = f.readlines()
#print(chars)
for i in chars:
	sfor = re.search(r' *for *(.*;.*;.*).*',i,re.M|re.I)
	sif=re.search(r' *if *(.*).*',i,re.M|re.I)
	swhile=re.search(r' *while *(.*).*',i,re.M|re.I)
	if sfor:
		#print("output...  "+sfor.group())
		k=sfor.group()
		sp=k.find(";")
		sp+=1
		ep=k.find(";",sp)
		sec_part=k[sp:ep]
		#print sec_part
		sp=k.find(")",ep+1)
		thr_part=k[ep+1:sp]
		#print thr_part
		thr_part = re.sub(' ','',thr_part)
		if sec_part.find('<') != -1 and (thr_part.find('-') !=-1 or thr_part.find('/') !=-1) :
			#print("hi")
			errors.append(i)
			kind.append(0)
		if sec_part.find('>') != -1 and (thr_part.find('+') != -1 or thr_part.find('*') != -1) :
			errors.append(i)
			kind.append(1)
		if sec_part.find('[') != -1:
			t1 = sec_part.find('[')
			t2 = sec_part.find(']',t1+1)
			x = sec_part[t1+1:t2]
			x = re.sub(' ','',x)
			idt1=re.match(r'[a-zA-Z][a-zA-Z0-9]*',x,re.M|re.I)	
		else:
			#print(sec_part)
			sec_part = re.sub(' ','',sec_part)
			#print(sec_part)
			idt1=re.match(r'[a-zA-Z][a-zA-Z0-9]*',sec_part,re.M|re.I)
		idt2=re.match(r'[a-zA-Z][a-zA-Z0-9]*',thr_part,re.M|re.I)
		if idt1:
			idt1=idt1.group(0)
		else:
			print("idt1 cant be found")
		if idt2:
			idt2=idt2.group(0)
		else:
			print("idt2 cant be found")
		#print("idt1: ",idt1)
		#print("idt2: ",idt2)
		if idt1 != idt2:
			errors.append(i)
			kind.append(2)

	if sif:
		k=sif.group()
		sp=k.find("(")
		sp+=1
		ep=k.find(")",sp)
		cond=k[sp:ep]
		if re.search(r'[^=<>!]=[^=]',cond,re.M|re.I):
			errors.append(i)
			kind.append(3)

	if swhile:
		k=swhile.group()
		sp=k.find("(")
		sp+=1
		ep=k.find(")",sp)
		sec_part=k[sp:ep]
		#print sec_part
		if sec_part.find('[') != -1:
			t1 = sec_part.find('[')
			t2 = sec_part.find(']',t1+1)
			x = sec_part[t1+1:t2]
			x = re.sub(' ','',x)
			idt1=re.match(r'[a-zA-Z][a-zA-Z0-9]*',x,re.M|re.I)	
		else:
			#print(sec_part)
			sec_part = re.sub(' ','',sec_part)
			#print(sec_part)
			idt1=re.match(r'[a-zA-Z][a-zA-Z0-9]*',sec_part,re.M|re.I)
		if idt1:
			idt1=idt1.group(0)
		else:
			print("idt1 cant be found")
		#print("idt1: ",idt1)

commands.getoutput("gcc -g Sol1.c -o outfile")
commands.getoutput("valgrind -v --track-origins=yes ./outfile 2>valg")
f=open("valg","r")
p=re.compile("Invalid write of size [\s0-9a-zA-Z=:().]*")
s=f.read()
l=p.findall(s)
p=re.compile("\(.*\.c.*\)")
hashmap={}
for i in l:
	k=p.findall(i)
	lineno=k[0].split(":")[1].split(")")[0]
	hashmap[lineno]=1

for i in hashmap.keys():
	print "In line "+i+" : "+chars[int(i)-1].strip()
	print "Possible use of unallocated memory"

for i in range(len(kind)):
	print("In line: "+errors[i]+ekind[kind[i]])
	# print(ekind[kind[i]])