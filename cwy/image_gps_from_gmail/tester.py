from image_downloader import *
from datetime import datetime

'''log test
g = connect_mail()
if g.logged_in == True:
	print("Succesfully logged in\n")
'''
#For Test
image_urls_dic = {'http://fl0ckfl0ck.info/jul.jpg': ['http://bit.ly/2MiFMhY>', datetime(2018, 8, 4, 10, 47, 36)], 'http://fl0ckfl0ck.info/%E1%84%88%E1%85%A9%E1%84%88%E1%85%B5.jpg': ['http://hoy.kr/SvCC', datetime(2018, 8, 5, 13, 50)], 'http://fl0ckfl0ck.info/%E7%A7%81%E3%81%AF%E4%BA%BA%E9%96%93%E3%81%AE%E5%B1%91%E3%81%A6%E3%82%99%E3%81%99.jpg': ['http://hoy.kr/N6DB', datetime(2018, 8, 5, 13, 50, 58)], 'http://fl0ckfl0ck.info/ga.jpg': ['http://bitly.kr/huvm', datetime(2018, 8, 4, 10, 47, 36)], 'http://fl0ckfl0ck.info/%EB%A7%9B%EC%9E%88%EC%96%B4.jpg': ['http://bitly.kr/nZXE', datetime(2018, 8, 4, 11, 24, 24)], 'http://fl0ckfl0ck.info/11.jpg': ['http://bitly.kr/jUa8', datetime(2018, 8, 2, 11, 23, 36)], 'http://fl0ckfl0ck.info/druwa.jpg': ['http://bit.ly/2OAwQWR\r\n', datetime(2018, 8, 3, 14, 34, 1)]}
#dirName=datetime.today().strftime("%Y-%m-%d")
dirName="2018-08-08"
#filenames = save_image(dirName, image_urls_dic)

#fileinfo_list = mark_in_map(dirName, filenames)
fileinfo_list = [['jul.jpg', 36.66294097222222, 126.62258911111111], ['\xe1\x84\x88\xe1\x85\xa9\xe1\x84\x88\xe1\x85\xb5.jpg', None, None], ['\xe7\xa7\x81\xe3\x81\xaf\xe4\xba\xba\xe9\x96\x93\xe3\x81\xae\xe5\xb1\x91\xe3\x81\xa6\xe3\x82\x99\xe3\x81\x99.jpg', None, None], ['ga.jpg', 37.527790083333336, 126.90460966666667], ['\xeb\xa7\x9b\xec\x9e\x88\xec\x96\xb4.jpg', 37.51306152777778, 127.05864716666666], ['11.jpg', None, None], ['druwa.jpg', 37.49848938888889, 127.01871491666667]]

fileinfo_list = make_csv(dirName,image_urls_dic,fileinfo_list)
print(fileinfo_list)
#make_csv(dirName,filenames)