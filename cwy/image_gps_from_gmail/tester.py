from image_downloader import *

'''log test
g = connect_mail()
if g.logged_in == True:
	print("Succesfully logged in\n")
'''
#For Test
image_urls_dic = {'http://fl0ckfl0ck.info/jul.jpg': 'http://bit.ly/2MiFMhY>\r', 'http://fl0ckfl0ck.info/%E1%84%88%E1%85%A9%E1%84%88%E1%85%B5.jpg': 'http://hoy.kr/SvCC', 'http://fl0ckfl0ck.info/%E7%A7%81%E3%81%AF%E4%BA%BA%E9%96%93%E3%81%AE%E5%B1%91%E3%81%A6%E3%82%99%E3%81%99.jpg': 'http://hoy.kr/N6DB', 'http://fl0ckfl0ck.info/ga.jpg': 'http://bitly.kr/huvm', 'http://fl0ckfl0ck.info/%EB%A7%9B%EC%9E%88%EC%96%B4.jpg': 'http://bitly.kr/nZXE', 'http://fl0ckfl0ck.info/11.jpg': 'http://bitly.kr/jUa8', 'http://fl0ckfl0ck.info/druwa.jpg': 'http://bit.ly/2OAwQWR\r\n'}
dirName=datetime.today().strftime("%Y%m%d")
filenames = save_image(dirName, image_urls_dic)
mark_in_map(dirName, filenames)