from bs4 import BeautifulSoup
import requests
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0','Connection': 'close'}
WEB= {
        1:'http://www.89ip.cn/index_1.html',
        2:'https://free-proxy-list.net',
        3:'https://api.proxyscrape.com/?request=share&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all',
      }
v = [2,3] #国外网站

# 请自行更换为自己SSR的端口，然后注释掉None
PROXIES = {'http':'127.0.0.1:1080',
        'https':'127.0.0.1:1080'}
PROXIES = None

def color(sign,args=''):
    colors = {'[-]':'\033[36m','[+]':'\033[32m','[!]':'\033[33m','[x]':'\033[31m'}
    if sign in colors:
        return colors[sign]+sign+args+'\033[0m'
    else: return    sign+args

def get_connect(url,proxies,r=''):
    n = 0
    while True:
        try:
            res = requests.get(url,headers=headers,proxies=proxies,timeout=5)
            return res.text
        except:
            if  r: 
                n +=1
                print('\r'+color('[!]',str(n)+' Try reconnect WEB %s        '%r),end='')
                if n == 3:
                    print('\r'+color('[x]',' reconnect  faild WEB %s        '%r),end='')
                    break
                else :  continue
            return  ''
    


def get_ips(rule,url) ->list:
    if rule == 1:
        return  r1(rule,url)
    elif rule ==2:
        return r2(rule,url)
    elif rule ==3:
        return r3(rule,url)

def msg(r):
    print('\r'+color('[-]','Try connect url %s          '%str(r)),end='')
    


def r1(rule,url):
    msg(rule)
    ip = []
    for i in range(1,12):
        url = 'http://www.89ip.cn/index_'+str(i)+'.html'
        html = get_connect(url,PROXIES,rule)
        if html:
            msg(str(rule)+'.'+str(i))
            soup = BeautifulSoup(html,'lxml')
            tr = soup.find(class_='layui-table').find_all('tr')
            for item in tr[1:]:
                ip.append(item.find_all('td')[0].string.strip()+':'+item.find_all('td')[1].string.strip())
    l = len(ip)
    if l :
        print(' total= %s'%l)
        return ip
    return ''

def r2(rule,url):
    msg(rule)
    html = get_connect(url,PROXIES,rule)
    if html:
        msg(rule)
        soup = BeautifulSoup(html,'lxml')
        tr = soup.find(id='list').find('tbody').find_all('tr')
        ip = []
        for item in tr:
            ip.append(item.find_all('td')[0].string+':'+item.find_all('td')[1].string)
        print(' total= %s'%len(ip))
        return ip
    return ''

def r3(rule,url):
    msg(rule)
    html = get_connect(url,PROXIES,rule)
    if html:
        msg(rule)
        page = re.search(r'(?<=paste :).*(?=\')',html).group()
        url = 'https://textitor.com/paste/'+page+'/plain'
        html = get_connect(url,PROXIES,2)
        html = html.split('\r\n')
        print(' total=%s'%len(html))
        return html[:-1]
    return ''

