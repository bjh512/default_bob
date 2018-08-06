def divide():
	with open('/media/bae/Elements/firewall.log', 'rb') as f:
		cnt = 0	
		for chunk in iter((lambda : f.read(2700000000)), ""):
			cnt = cnt + 1
			newf = open("../firewall"+str(cnt)+'.log','w')
			newf.write(chunk.decode('utf-8'))
			print("firewall"+str(cnt)+" is created!")
			newf.close()


def test_divided():
	with open('../firewall20.log') as f:
		for line in f:
			print(line)

#test_divided()
divide()