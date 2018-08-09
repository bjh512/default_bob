#-*- coding: utf-8 -*-
from gmail import Gmail
import base64
import requests
import sys
from urllib import quote,unquote
import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import pandas as pd
import hashlib

reload(sys)
sys.setdefaultencoding('utf-8')
exten_list = ["jpg", "jpeg", "tif", "tiff"]

def connect_mail():
	with open('account.txt','r') as f:
		account = f.readline()
		id = account.split()[0]
		pw = account.split()[1]

	#login
	g = Gmail()
	g.login(id,pw)
	
	return g

def chase_redirects(url):
	while True:
		yield url
		r = requests.head(url)
		if 300 < r.status_code < 400:
			url = r.headers['location']
		else:
			break

def make_url_dict(mails):
	#read mails
	mail_bodies = list()
	image_urls_dic = dict()

	for amail in mails:
		amail.fetch()
		body = (amail.body, amail.sent_at)
		mail_bodies.append(body)

	for body,time in mail_bodies:
		print("-----------From this mail------------")
		print(body)
		print("---------------Result----------------")

		#make a index list of slahses
		list_slashes = list()
		for i,char in enumerate(body):
			if(char=="/"):
				list_slashes.append(i)
		for j in list_slashes:
			if j-1 not in list_slashes and j+1 not in list_slashes:
				#from "(4)/(1)" to "(9)/(9)"
				offset = 1
				for ind_left in range(offset+3,10):
					for ind_right in range(offset,10):
						url = "http://"+body[j-ind_left:j]+body[j]+body[j+1:j+ind_right+1]
						#try to connect
						try:
							#repeatedly redirect using generator "yield"
							for url_ in chase_redirects(url):
								#print(url_)
								req = requests.head(url_, timeout=3)
								code_http_resp = req.status_code
								#if 200 and exif => to the dict
								if code_http_resp == 200:
									for exten in exten_list:
										if exten in url_:
											if url.endswith("\r\n"):
												url=url.strip("\r\n")
											elif url.endswith("\r"):
												url=url.strip("\r")
											image_urls_dic[url_] = [url,time]
											print("Image url uploaded")	

						except Exception as e:
							'''
							print("Failed to connect the url")
							print(e)
							'''
							pass

	return image_urls_dic


def save_image(dirName, image_urls_dic):
	try:
		os.mkdir(dirName)
		print(dirName+" dir is created")
	except Exception as e:
		if str(e)=="[Errno 17] File exists: '"+dirName+"'":
			print(dirName+" dir is already existed")
			pass
	filenames = []
	for url in image_urls_dic.keys():
		filename = url.split('/')[-1]
		filename = unquote(filename)
		r = requests.get(url, allow_redirects=True)
		open("./"+dirName+"/"+filename, 'wb').write(r.content)
		print(filename)
		filenames.append(filename)

	return filenames


def mark_in_map(dirName, filenames):
	kmlheader = '<?xml version="1.0" encoding="UTF-8"?>' + '<kml xmlns="http://www.opengis.net/kml/2.2">'
	with open('on_the_map.kml', "w+") as f:
	    f.write(kmlheader)

	fileinfo_list = []
	for filename in filenames:
		try:
			img = Image.open("./"+dirName+"/"+filename)
			info = img._getexif()
			exif = {}
			for tag, value in info.items():
			    decoded = TAGS.get(tag, tag)
			    exif[decoded] = value
			# from the exif data, extract gps
			exifGPS = exif['GPSInfo']
			latData = exifGPS[2]
			lonData = exifGPS[4]
			# calculae the lat / long
			latDeg = latData[0][0] / float(latData[0][1])
			latMin = latData[1][0] / float(latData[1][1])
			latSec = latData[2][0] / float(latData[2][1])
			lonDeg = lonData[0][0] / float(lonData[0][1])
			lonMin = lonData[1][0] / float(lonData[1][1])
			lonSec = lonData[2][0] / float(lonData[2][1])
			# correct the lat/lon based on N/E/W/S
			Lat = (latDeg + (latMin + latSec / 60.0) / 60.0)
			if exifGPS[1] == 'S': Lat = Lat * -1
			Lon = (lonDeg + (lonMin + lonSec / 60.0) / 60.0)
			if exifGPS[3] == 'W': Lon = Lon * -1
			# print file
			#msg = "There is GPS info in this picture located at " + str(Lat) + "," + str(Lon)
			#print(msg)
			kml = '<Placemark><name>%s</name><Point><coordinates>%6f,%6f</coordinates></Point></Placemark>' % (
			filename, Lon, Lat)
			with open('on_the_map.kml', "a") as f:
			    f.write(kml)
			print("kml file created")
			print(filename)
			fileinfo_list.append([filename,Lat,Lon])
		except:
			print("There is no GPS info in this picture")
			fileinfo_list.append([filename,None,None])
			pass
	with open('on_the_map.kml',"a") as f:
		f.write("</kml>")

	return fileinfo_list


def file_hash(dirName, filename):
	hasherM = hashlib.md5()
	hahserS1 = hashlib.sha1()
	with open('./'+dirName+'/'+filename,'rb') as afile:
		buf = afile.read()
		hasherM.update(buf)
		hahserS1.update(buf)
		(hasherM.hexdigest())
	return (hasherM.hexdigest(),hahserS1.hexdigest())

def make_csv(dirName, image_urls_dic, fileinfo_list):
	#combine 2 data sets
	for key in image_urls_dic.keys():
		for index,info in enumerate(fileinfo_list):
			#print(key.split('/')[-1], info[0])
			if unquote(key.split('/')[-1])==info[0]:
				fileinfo_list[index].append(key)
				fileinfo_list[index].append(image_urls_dic[key][0])
				fileinfo_list[index].append(image_urls_dic[key][1])
				md5,sha1 = file_hash(dirName, info[0])
				fileinfo_list[index].append(md5)
				fileinfo_list[index].append(sha1)

	#rearrange the array
	fileinfo_order = [5,4,3,0,1,2,6,7]
	for index in range(len(fileinfo_list)):
		fileinfo_list[index] = [fileinfo_list[index][i] for i in fileinfo_order]

	csv_header = ["Date","Shortened URL","Full URL","FileName","Latitude","Longitude","MD5","SHA1"]
	df = pd.DataFrame(data=fileinfo_list,columns=csv_header)
	df.to_csv("./"+dirName+"/result.csv")

	return fileinfo_list


def disconnect_mail(g):
	#logout
	g.logout()
	if g.logged_in == False:
		"Succesfully logged out"


if __name__ == '__main__':

	dirName = datetime.today().strftime("%Y-%m-%d")

	#connect to my gmail account
	g = connect_mail()
	if g.logged_in == True:
		print("Succesfully logged in\n")
	
	#load directories' name for getting mails after last day
	direc_list = [name for name in os.listdir(".") if os.path.isdir(name)]
	direc_list.sort()

	if dirName in direc_list:
		direc_list.pop(direc_list.index(dirName))

	if len(direc_list) == 0:
		mails = g.inbox().mail(sender="fl0ckfl0ck@hotmail.com")
	elif len(direc_list) >= 1:
		last_date = datetime((int)(direc_list[-1][:4]),(int)(direc_list[-1][5:7]),(int)(direc_list[-1][8:]))
		mails = g.inbox().mail(sender="fl0ckfl0ck@hotmail.com", after=last_date)

	#extract urls
	image_urls_dic = make_url_dict(mails)
	
	#save images in a folder
	filenames = save_image(dirName, image_urls_dic)
	fileinfo_list=mark_in_map(dirName, filenames)

	#create csv file in each date folder by using 2 data sets
	fileinfo_list=make_csv(dirName, image_urls_dic,fileinfo_list)
	print(fileinfo_list)
	
	disconnect_mail(g)