from concurrent.futures import ThreadPoolExecutor
import time, requests, math, shutil, threading, os, sys, getopt
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
hrefs = []   #存放所有图片链接的地址
n = 0       #爬取张数

def color(sign,args=''):
    colors = {'[+]':'\033[32m','[!]':'\033[33m','[-]':'\033[36m'}
    if sign not in colors:
        return sign+args
    else:
        return colors[sign]+sign+args+'\033[0m'

#获取页面的HTML代码
def get_html(url):
    try:
        res = requests.get(url,headers=headers,timeout=3)
        if res.status_code == 200:
          return res
        else: return 0
    except:
        return 0

#从页面爬取封面图片的地址
def  img_url(i):   
    global hrefs
    for item in range(1,i):
        item = str(item)
        url = "https://wallhaven.cc/search?sorting=views&page="+item
        print('\r'+color('[-]',"Try to connect Page %s"%item),end='')

        html = get_html(url)
        while html == 0 :
            print('\r'+color('[!]',"Try to reconnect Page %s"%item))
            html = get_html(url)
        html = html.text
        soup = BeautifulSoup(html,'lxml')
        li = soup.find(id='thumbs').find(class_ = 'thumb-listing-page').find_all('li')
        for i in li:
                href = i.find('a').get('href')
                hrefs.append(href)

 #获取图片链接
def download_url(url,i):    
        html = get_html(url)
        while html == 0 : 
            html = get_html(url)
        html = html.text
        soup = BeautifulSoup(html,'lxml')
        h = soup.find(id='wallpaper').get('src')
        download(h,i)

#通过图片链接保存图片到本地
def download(url,i):           
    global n
    filename = i+".jpg"
    html = get_html(url)
    while html == 0:
        html = get_html(url)
    with open(filename,'wb') as f:
        html = html.content
        f.write(html)
        n -=1
    print('\r'+color('[-]',"%s  completed | %s  left    "%(i,str(n))),end='')

#创建线程池提高爬虫效率
def pool(img_url,works):          
    global n
    ends = n
    start_time = time.time()
    with  ThreadPoolExecutor(works) as exector :          #设置线程数
        j = 1
        for url in img_url[:ends]:
            exector.submit(download_url,url,str(j))    #提交给线程池要执行的任务
            j += 1
    end_time = time.time()
    times = round((end_time-start_time)/60,2)
    print('\n'+color('[+]',"Takes %s m "%str(times)))
        
def usage():
    print('-n    爬取张数\n-t    开启线程数\n-f    保存文件名\n 默认30线程，文件名为images')
    sys.exit(0)
 
def main():
    global n
    works = 30
    filename = 'images'
    if not len(sys.argv[1:]):
        usage()
    try: 
        options,args = getopt.getopt(sys.argv[1:],'n:t:f:')
    except getopt.GetoptError as e:
        print(str(e))
        usage()
    for name, value in options:
        if name =='-n':
            n = int(value)
        elif name == '-t':
            works = int(value)
        elif name == '-f':
            filename = value
        else:
            assert False,'unhandled option'
    
    page = math.ceil(n/24)+1
    img_url(page)
    print('\n'+color('[+]','Ready to download...'))
    try:
      shutil.rmtree(filename) #删除已存在文件夹和文件夹下所有文件
    except:pass
    os.mkdir(filename)
    os.chdir(filename)
    pool(hrefs,works)

if __name__ == '__main__':
    main()
