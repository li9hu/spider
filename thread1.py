# encoding=utf-8
import threading
import time

class  MyThread(threading.Thread):
    def __init__(self, name, id, count):
        threading.Thread.__init__(self)
        self.name  = name
        self.id = id
        self.count = count

    def run(self):
        print("线程开始 by+ "+self.name)
        go(self.name,self.count)
        print("线程结束 by +"+self.name)


def go(name,count):
    while count:
        time.sleep(1)
        print("o o o "+str(int(time.time())))
        count -=1

def main():
    thread1 = MyThread('lx','1',4)
    thread2 = MyThread('ly','2',7)
    thread1.start()
    thread2.start()
    thread2.join()
    thread1.join()
    print("--------")

if __name__ == '__main__':
    main()
    
