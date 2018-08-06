import os

for i in range(4000000,4168269):
	string = "rm ../firewall"+str(i)+".log"
	os.system(string)
	print(str(i)+"is deleted")