import re
import sys

with open("./rime.txt",'r') as f:
	#I had tested this program using print function when developing, so I just redirected stdout to a result file.
	sys.stdout = open("./rime.html",'w')
	origin_lines = f.readlines()
	#Put some html's headers.
	print('<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml">\n <head>')
	'''
	There are some rules only used in top of the file, so I divided it two parts.
	And before the 2nd <p> tag, there is no <br/> but after that I should change every blank line to <br/>
	That is another reason for using flag called "is_header"	
	'''
	is_header = True
	for line in origin_lines:
		#For the title tag
		regex_t = re.compile("^[A-Z]{3}[\s][A-Z]{4}.*")
		#For h2 tags
		regex_h2 = re.compile('^([A-Z]{5,}|I{0,3}V?I{0,2}\.)')
		#For the 1st p tag
		regex_p = re.compile('^.+;.+;.+;.+')
		#For the start of the 2nd p tag
		regex_ps = re.compile('^[ ]*It is an ')
		#For the end of the 2nd p tag
		regex_pe = re.compile('^[ ]*(.*)He rose the')
		#For br tags after the 2nd p tag
		regex_br = re.compile('^.+\n|^$')

		if is_header == True:
			if regex_t.search(line):
				print("  <title>"+line[:-1]+"</title>")
				print('  <meta charset="utf-8"/>\n </head>\n<body>')
				print('<h1>'+line[:-1]+"</h1>")
				print(line)
			
			elif regex_h2.search(line):
				print('<h2>'+line[:-2]+'</h2>\n')
			
			elif regex_p.search(line):
				print('<p>'+line[:-1]+'</p>\n')
			
			elif regex_ps.search(line):
				print('  <p>'+line[5:-1]+'<br/>')
				is_header = False

		else:
			if regex_pe.search(line):
				print(line+'</p>')
			
			elif regex_h2.search(line):
				print('<h2>'+line[:-2]+'</h2>')

			elif regex_br.search(line):
				#Handling some exception lines
				if "slay" in line or "high;" in line:
					print(line[:-1])
				else:
					print(line[:-1]+'<br/>')
	
	print(" </body>")
	print("</html>\n")
	sys.stdout.close()