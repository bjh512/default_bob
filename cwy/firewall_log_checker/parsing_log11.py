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
		with open('error_log11.log','w') as logfile:
			for i in range(0,len(line)):
				logfile.write('\n'+str(line[i])+'\n')
				if line[i][:5]=='2018-':
					break

		offset = -1
		for j in range(i,len(line)):
			offset = offset + len(line[j]) +1

		f.seek(-int(offset),1)
		
		flag=False

		for chunk in iter(lambda : str(f.read(323)), ""):
			try:
				i = i+1
				line = chunk.split(" ")

				#Fuck that no equal
				if "90" in line[:-1]:
					print(chunk)
					print(line.pop(11))
					print(line.pop(11))
					print(line)

				#Fuck that sy
				if "sy" in line[:-1]:
					print(chunk)
					if line.pop(6) == '' and line[6]=='SecureNet':
						line[5]=line[5]+line[6]
						for log11i in range(6,18):
							line[log11i]=line[log11i+1]
						line.pop(18)
					print(line)

				#Fuck that sy2018
				if "sy2018-06-28" in line[:-1]:
					try:
						line.pop(0)
						line.pop(0)
						line.pop(0)
						line.pop(0)
						line.pop(0)
						line[0] = line[0][2:]
					except:
						line.pop()
						line[0] = line[0][2:]

				if flag==True:
					line.pop(0)
					flag=False


				time_tuple = (int(line[0][:4]), int(line[0][5:7]), int(line[0][-2:]), int(line[1][:2]), int(line[1][3:5]), int(line[1][-2:]),0,0,0)
				tmp.append(int(time.mktime(time_tuple)))

				#God damn space in ip address
				if len(line[13])<15 and len(line[14])<6:
					line[13]=line[13]+".8"+line[15]
					for log11i in range(14,18):
						line[log11i]=line[log11i+2]
					line.pop(18)
					line.pop(18)

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

				try:
					tmp_prt = line[17].split("=")[1]
					tmp.append(int(tmp_prt))
				except:
					tmp.append(48212)
					flag = True

				tmp_act = line[9].split("=")[1]
				tmp.append('"' + tmp_act + '"')

			except Exception as e:
				with open('error_log_in_split.log11','ab') as logfile:
						print(tmp)
						logfile.write(str(e)+"\n")
						logfile.write(chunk+"\n")
						for fucking_index, fucking_space in enumerate(line):
							logfile.write(" ["+str(fucking_index)+"] "+fucking_space)
				sys.exit()

			placeholders.append(','.join(str(x) for x in tmp))
			try:
				if line[18]:
					count = 0
					count = count + len(line)-19
					for j in range(18,len(line)):
						count = count + len(line[j])
			except Exception as e:
				with open('error_log_at_each_segment_file.log11', 'ab') as logs:
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
						
				for index,row in enumerate(placeholders):
					try:
						sql = "insert into firewall11_log ({0}) values ({1});".format(columns, row)
						cursor.execute(sql)

					except Exception as e:
						with open('error_log_in_sql.log11','ab') as logfile:
							print("ERROR!")
							print(e)
							print(row)
							logfile.write(str(e)+"\n")
							for logi, logr in enumerate(placeholders):
								logfile.write(str(logi)+" "+logr+"\n")
							sys.exit()
							#logfile.write(str(index-1)+placeholders[index-1]+'\n')
							#logfile.write(str(index)+"row : "+row+"\n")
						#pass
		
				conn.commit()
				#print("A bunch of data is succesfully executed.")
				conn.close()
				i = 0
				placeholders=[]

	print(str(logfile_num)+" th is finished.")