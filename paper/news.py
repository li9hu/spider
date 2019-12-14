import rules
import requests
from bs4 import BeautifulSoup
import xlwt

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}


def choose(url,soup,t):
	if t == 'xianzhi':
		rules.xianzhi(url,soup)
	elif t == 'anquanke':
		anquanke(url,soup)
	


def spider(url,t):
	if 1 :
		res = requests.get(url,headers=header,timeout=1)
		if res.status_code == 200:
			html = res.text
			soup = BeautifulSoup(html,'lxml')
			choose(url,soup,t)
			
			
#	except:
#		print('ERROR!')

def main():
	url = 'https://xz.aliyun.com'
	t = 'xianzhi'
	spider(url,t)

if  __name__ == '__main__':
	main()
