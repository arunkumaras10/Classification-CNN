from flask import Flask, render_template,request
import flask
import string
import commands
import json
import re
app = Flask(__name__)
@app.route("/")
def main():
    return render_template('index.html')

@app.route("/predictSolution.html", methods = ['GET'])
def predictSolutionHTML():
	return render_template('predictSolution.html')

@app.route("/tagProblem", methods = ['POST'])
def tagProblem():

	# get problem id from form element
	problem=request.form['probid']

	s=commands.getoutput("python tagProblem.py "+problem)
	print s
	lines=s.split("\n")
	n=0
	for i in lines:
		n+=1
	s=lines[n-1]
	print 'response will be '+s
	return flask.Response(s,mimetype="text/html")


@app.route("/predictSolution", methods = ['POST'])
def predictSolution():

	# get code from form element
	code=request.form['code']

	# write code to temp file

	newfile=open('temp','w')
	newfile.write(code)
	newfile.close()


	s=commands.getoutput("python predict.py")
	lines=s.split("\n")
	n=0
	for i in lines:
		n+=1
	s=lines[n-1]
	return flask.Response(s,mimetype="text/html")


@app.route("/recommend", methods = ['POST'])
def recommend():
	# get problem id from form element
	# print request.form.keys()
	problem=request.form['problemid']

	print '---------------'
	print problem

	s=commands.getoutput("python recommend.py "+problem)
	print s
	lines=s.split("\n")
	n=0
	for i in lines:
		n+=1
	r={}
	r[0]=lines[n-3]
	r[1]=lines[n-2]
	r[2]=lines[n-1]

	prob={}
	section={}

	i=0

	while i<3:
		#processing the problem id
		reg = re.compile("([0-9]+)([a-zA-Z]+)")
		m = reg.match(r[i])
		prob[i] = m.group(1)
		section[i] = m.group(2)
		i+=1

	s=commands.getoutput("python storeSourceCodes.py "+r[0]+" "+r[1]+" "+r[2])
	print s

	s=commands.getoutput("python sanitize.py")
	print s
	
	return render_template('recommend.html',prob=problem,prob1=prob[0],prob2=prob[1],prob3=prob[2],sec1=section[0],sec2=section[1],sec3=section[2])

@app.route("/hints.html", methods = ['POST'])
def hintsHTML():
	prob=request.form['problemid']
	return render_template('hints.html',probid=prob)


@app.route("/logicalErrors", methods = ['POST'])
def logicalErrors():

	# get code from form element
	code=request.form['code']

	# write code to temp file

	newfile=open('Sol1.c','w')
	newfile.write(code)
	newfile.close()


	s=commands.getoutput("python logical.py")	
	return flask.Response(s,mimetype="text/html")

@app.route("/generateHint1", methods = ['POST'])
def generateHint1():


	problem=request.form['probid']
	print "id= "+problem
	s=commands.getoutput("python findTricks.py "+problem)	
	print s

	return flask.Response(s,mimetype="text/html")


if __name__ == "__main__":
    app.run()