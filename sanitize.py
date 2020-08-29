import re

f=open('src1.html','r')
chars=f.read()
f.close()

chars=re.sub('<script[^<]*(?:(?!<\/script>)<[^<]*)*</script>','',chars)


f=open('./static/html/sanitizedsrc1.html','w')
f.write(chars)
f.close()

f=open('src2.html','r')
chars=f.read()
f.close()

chars=re.sub('<script[^<]*(?:(?!<\/script>)<[^<]*)*</script>','',chars)


f=open('./static/html/sanitizedsrc2.html','w')
f.write(chars)
f.close()

f=open('src3.html','r')
chars=f.read()
f.close()

chars=re.sub('<script[^<]*(?:(?!<\/script>)<[^<]*)*</script>','',chars)


f=open('./static/html/sanitizedsrc3.html','w')
f.write(chars)
f.close()