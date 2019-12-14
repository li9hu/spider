from concurrent.futures import ThreadPoolExecutor
import time
import requests
import math
import shutil
import threading
import os
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
#请自行修改自己得SSR代理端口
proxies = {'https':'127.0.0.1:1080',
            'http':'127.0.0.1:1080'
        }
hrefs = []   #存放所有图片链接的地址
n = 0       #爬取张数
have = []   # 查看剩余多少下载

#获取页面的HTML代码
def get_html(url):
    try:
        res = requests.get(url,headers=headers,proxies=proxies,timeout=3)
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
        print("[-] 正在尝试连接Page "+item)
        html = get_html(url)
        while html == 0 : 
            print("[!] 尝试重新连接Page "+item)
            html = get_html(url)
        print("[+] 连接成功")
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
            print("[!] 尝试重新连接 img"+str(i))
            html = get_html(url)
        html = html.text
        soup = BeautifulSoup(html,'lxml')
        h = soup.find(id='wallpaper').get('src')
        download(h,i)

#通过图片链接保存图片到本地
def download(url,i):           
    global have
    print("[+] downloading img "+i)
    filename = i+".jpg"
    html = get_html(url)
    while html == 0:
        print("[-] 尝试重新下载 img"+i)
        print("[+] Remainnig: %s"% (have))
        html = get_html(url)
    with open(filename,'wb') as f:
        html = html.content
        f.write(html)
    have.remove(int(i))
    print("[+] Remainnig: %s"% (have))

#创建线程池提高爬虫效率
def pool(img_url,works):          
    global n
    start_time = time.time()
    with  ThreadPoolExecutor(works) as exector :          #设置线程数
        j = 1
        for url in img_url[:n]:
            exector.submit(download_url,url,str(j))    #提交给线程池要执行的任务
            j += 1
    end_time = time.time()
    print("\n耗时: "+str(end_time-start_time))

def main():
    global n
    global have
    n = int(input("想爬多少张: "))
    works = int(input("想开启的线程数: "))
    have=list(range(1,n+1))  
    i = math.ceil(n/24)+1
    img_url(i)
    print("[+] 正在准备下载...")
    name = 'images'  #文件夹名
    try:
      shutil.rmtree(name) #删除文件夹和文件夹下所有文件
    except:pass
    os.mkdir(name)
    os.chdir(name)
    pool(hrefs,works)
    print('[+] Download Over!')

if __name__ == '__main__':
    main()
