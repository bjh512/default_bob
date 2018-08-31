from bs4 import BeautifulSoup
from urllib.request import *
import wget
from zipfile import ZipFile
import os
import pygeoip
import csv

def down_html():
	url = 'http://fl0ckfl0ck.info/cert/'
	wget.download(url)


def extractor():
	with open('./index.html','r') as f:
		soup = BeautifulSoup(f,features="html.parser")
		with open('./text.txt','w') as output:
			output.write(soup.text)


def downloader():
	with open('./text.txt') as f:
		cert_list = dict()
		lines = f.readlines()
		base_url = 'http://fl0ckfl0ck.info/cert/'

		for line in lines:
			zip_name = line[:-24]
			cert_list[zip_name] = {'time' : line[-24:-8]}
			try:
				wget.download(base_url+zip_name)
			except Exception as e:
				with open('./error_log.txt', 'a') as logf:
					print(str(e))
					print("Error with "+zip_name)
					logf.write(str(e) + " " + zip_name)
		#print(cert_list)

def unzipper():
	with open('./text.txt') as f:
		cert_list = list()
		lines = f.readlines()
		cnt = 0

		for line in lines:
			cnt += 1
			zip_name = line[:-24]
			with ZipFile("./zip_folder/"+zip_name,"r") as azip:
				with open('./certs/'+str(cnt)+"_"+line[-24:-8]+"_"+line[:-28],'wb') as acert:
					acert.write(azip.read('signCert.cert'))


def make_csv():
	certlist = os.listdir('./certs/')
	gi = pygeoip.GeoIP('GeoLiteCity.dat')
	gid = pygeoip.GeoIP('GeoIP.dat')
	data_list = list()
	data_list.append(['Serial','Upload_time','Name','Bank','Account','IP','Country'])

	for certname in certlist:
		with open('./certs/'+certname,"rb") as acert:
			content = acert.read().decode('cp949')
			title_parse = certname.split('_')
			
			serial,upload_time,ip = title_parse
			name = content.split('()')[0].split('=')[1]
			bank = content.split(',')[1].split('=')[1]
			account = content.split(',')[0].split('()')[1]+"padding"
			try:
				country = gid.country_name_by_addr(ip)
			except Exception as e:
				with open('./error_log.txt','w') as logf:
					logf.write(str(e))
					lgof.write("Error on "+serial)
					print(str(e))

			#Showing progress
			print(serial)

		data_list.append([serial, upload_time, name, bank, account, ip, country])

	with open('./cert_csv.csv', 'w') as resultf:
		writer = csv.writer(resultf, quoting=csv.QUOTE_ALL)
		for data in data_list:
			writer.writerow(data)

if __name__ == '__main__':

	#I executed each function in this order.

	#down_html()
	#extractor()
	#downloader()
	#unzipper()
	make_csv()