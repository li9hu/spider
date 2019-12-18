import   sys
import time
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED
from rules import *

total = 0
ok = []
save = ''

def check(ip):
    global ok
    global save
    global total
    proxies = {'http':ip}
    url = 'http://pv.sohu.com/cityjson?ie=utf-8'
    print('\r'+color('[+]','got %s   '%str(total)),end='')
    html = get_connect(url,proxies)
    if html:
        ip1 = re.findall(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}',html)[0]
        ip2 = ip.split(':')[0]
        if ip1 == ip2:
            total +=1
            print('\r'+color('[+]','got %s   '%str(total)),end='')
            ok.append(ip)
            save.write(ip+'\n')

def check_pool(check_ip):
    global save
    global total
    global ok
    open('ip.txt','w').write('')
    save = open('ip.txt','a')
    start_time = time.time()
    with ThreadPoolExecutor(200) as exector:
        for ip in check_ip:
            exector.submit(check,ip)
    save.close()
    end_time = time.time()
    times = round((end_time-start_time)/60,2)
    print('\n'+color('[+]','Takes %s m'%str(times)))
    c = input(color('[-]','want to keep checking? [y/n] ')).lower()
    if c in 'y':
        s = ok
        total = 0
        ok = []
        check_pool(s)


def main():
    check_ip = []
    if PROXIES == None: print(color('[!]','Please modify PROXIES in rules.py or you have only few proxies!'))
    for  rule,url in WEB.items():
        if rule  in v and PROXIES == None: continue
        check_ip += get_ips(rule,url)
    if check_ip :
        check_ip = list(set(check_ip))
        print('\n\n'+color('[+]','Check This proxies...'))
        check_pool(check_ip)

if __name__ == '__main__':
    main()
