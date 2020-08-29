import urllib
import sys
import re
prob_name={}

prob_name[0]=str(sys.argv[1])
prob_name[1]=str(sys.argv[2])
prob_name[2]=str(sys.argv[3])

i=1

while i<=3:
	#processing the problem id
	r = re.compile("([0-9]+)([a-zA-Z]+)")
	m = r.match(prob_name[i-1])
	problem = m.group(1)
	section = m.group(2)

	proburl='http://codeforces.com/problemset/problem/{prob}/{sec}'

	print 'reading...'+prob_name[i-1]
	code= urllib.urlopen(proburl.format(prob=problem,sec=section)).read()
	print 'read'

	file=open('src'+str(i)+'.html','w')
	file.write(code)
	file.close()

	i+=1

print 'success'


	