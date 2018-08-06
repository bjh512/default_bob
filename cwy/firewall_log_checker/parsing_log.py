import pymysql
import time
import socket
import sys

for logfile_num in range(11,12):
	with open('../firewall'+str(logfile_num)+".log") as f:
		tmp = list()
		placeholders = list()
		i=0
		chunk = str(f.read(280))
		line = chunk.split(" ")
		with open('error_log.log','ab') as logfile:
			for i in range(0,len(line)):
				logfile.write(str(line[i]))
				if line[i][:5]=='2018-':
					break

		offset = -1
		for j in range(i,len(line)):
			offset = offset + len(line[j]) +1

		f.seek(-int(offset),1)
		

		for chunk in iter(lambda : str(f.read(300)), ""):
			try:
				i = i+1
				line = chunk.split(" ")
				time_tuple = (int(line[0][:4]), int(line[0][5:7]), int(line[0][-2:]), int(line[1][:2]), int(line[1][3:5]), int(line[1][-2:]),0,0,0)
				tmp.append(int(time.mktime(time_tuple)))

				tmp_ip = line[13].split("=")[1].replace(".","")
				tmp.append(int(tmp_ip))
				
				tmp_ip = line[14].split("=")[1].replace(".","")
				tmp.append(int(tmp_ip))

				tmp_mac = line[11].split("=")[1]
				tmp.append('"' + tmp_mac + '"')

				tmp_mac = line[12].split("=")[1]
				tmp.append('"' + tmp_mac + '"')

				tmp_len = line[15].split("=")[1]
				tmp.append(int(tmp_len))

				tmp_prt = line[16].split("=")[1]
				tmp.append(int(tmp_prt))

				tmp_prt = line[17].split("=")[1]
				tmp.append(int(tmp_prt))

				tmp_act = line[9].split("=")[1]
				tmp.append('"' + tmp_act + '"')

			except Exception as e:
				if e == "list index out of range":
					with open('error_log.log','ab') as logfile:
							logfile.write(e)
							logfile.write(chunk)
				pass

			placeholders.append(','.join(str(x) for x in tmp))
			try:
				if line[18]:
					count = 0
					count = count + len(line)-19
					for j in range(18,len(line)):
						count = count + len(line[j])
			except Exception as e:
				with open('error_log_at_each_segment_file', 'ab') as logs:
					logs.write(str(e))
					try:
						for logging_index in range(0,18):
							log.write(line[logging_index])
					except:
						pass
					count=0
					i=1000
					placeholders = placeholders[:-1]
				pass


			f.seek(-int(count),1)

			tmp = []

			if i >= 1000:
				conn = pymysql.connect(host='localhost', user='bae', passwd='', db='bob')
				cursor = conn.cursor()

				columns = "datetime, src_ip, dst_ip, src_mac, dst_mac, length, src_port, dst_port, action"
						
				for row in placeholders:
					try:
						print(row)
						sql = "insert into firewall_log ({0}) values ({1});".format(columns, row)
						cursor.execute(sql)

					except Exception as e:
						with open('error_log.log','ab') as logfile:
							print("ERROR!")
							print(e)
							print(row)
							logfile.write(str(e)+row + "\n")
						break
						#pass
		
				conn.commit()
				#print("A bunch of data is succesfully executed.")
				conn.close()
				i = 0
				placeholders=[]

	print(str(logfile_num)+"th is finished.")