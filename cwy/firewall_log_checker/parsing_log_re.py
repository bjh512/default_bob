import pymysql
import time
import socket

#Hell efficiency.. 10M lines with 8 hr..
with open('../firewall1.log') as f:
	tmp = dict()

	#ip*2, length, port*2, 
	chunk = f.read()
	chunk = chunk.split("2018-")
	line = list()

	conn = pymysql.connect(host='localhost', user='bae', passwd='', db='bob')

	for line in chunk:
		cursor = conn.cursor()

		if line =='':
			continue

		line = line.split(" ")
		
		time_tuple = (2018, int(line[0][0:2]), int(line[0][-2:]), int(line[1][:2]), int(line[1][3:5]), int(line[1][-2:]),0,0,0)
		tmp["datetime"] = int(time.mktime(time_tuple))

		tmp_ip = line[13].split("=")[1].replace(".","")
		tmp["src_ip"] = int(tmp_ip)
			
		tmp_ip = line[14].split("=")[1].replace(".","")
		tmp["dst_ip"] = int(tmp_ip)

		tmp_mac = line[11].split("=")[1]
		tmp["src_mac"] = '"' + tmp_mac + '"'

		tmp_mac = line[12].split("=")[1]
		tmp["dst_mac"] = '"' + tmp_mac + '"'

		tmp_len = line[15].split("=")[1]
		tmp["length"] = int(tmp_len)

		tmp_prt = line[16].split("=")[1]
		tmp["src_port"] = int(tmp_prt)

		tmp_prt = line[17].split("=")[1]
		tmp["dst_port"] = int(tmp_prt)

		tmp_act = line[9].split("=")[1]
		tmp["action"] = '"' + tmp_act + '"'

		line.clear()

		columns = ''
		placeholders = ''
			
		for k,v in tmp.items():
			placeholders = placeholders + str(v) +','
			columns = columns + str(k) + ','
		placeholders = placeholders[:-1]
		columns = columns[:-1]

		try:
			sql = "insert into firewall_log ({0}) values ({1});".format(columns, placeholders)
			print(sql)
			cursor.execute(sql)
		except Exception as e:
			print("ERROR!")
			print(e)
			pass
			
		conn.commit()	
	conn.close()

	if len(line) != 0:
		print(line)