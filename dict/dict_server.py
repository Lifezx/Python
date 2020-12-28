'''
在线词典 服务端

* 处理业务逻辑
* 多进程并发模型
'''

from socket import *
from multiprocessing import Process
import sys,signal
from dict_db import User
from time import sleep


HOST = '127.0.0.1'
PORT = 8000
ADDR = (HOST,PORT)
user = User('dict')


# 处理客户端各种请求
def request(connfd):
    user.create_cursor() # 每个子进程有自己的游标
    while True:
        data = connfd.recv(1024).decode() # 接收请求
        index = data.split(' ')[0]
        if not data or index == 'E':
            sys.exit()
        elif index == 'L':
            login(connfd,data.split(' ')[1],data.split(' ')[2])
        elif index == 'R':
            register(connfd,data.split(' ')[1],data.split(' ')[2])
        elif index == 'S':
            seek_word(connfd,data.split(' ')[1],data.split(' ')[2])
        elif index == 'H':
            history(connfd,data.split(' ')[1])
        elif index == 'Q':
            pass

def register(connfd,name,password):
    if user.register(name,password):
        connfd.send(b'ok')

def login(connfd,name,password):
    if user.login(name,password):
        connfd.send(b'ok')

def seek_word(connfd,word,name):
    mean = user.seek_word(word,name)
    if not mean:
        connfd.send('没有找到该单词'.encode())
    else:
        insert_history(word,name)
        connfd.send(mean.encode())

def insert_history(word,name):
    user.insert_history(word,name)

def history(connfd,name):
    history_tuple = user.history(name)
    for i in history_tuple:
        msg = "%s   %-16s   %s"%i
        connfd.send(msg.encode())
        sleep(0.1)
    connfd.send(b'##')


# 搭建网络
def main():
    # 创建套接字
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(ADDR)
    sockfd.listen(5)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    # 循环等待客户端连接
    print('Listen the port 8000')
    while True:
        try:
            c,addr = sockfd.accept()
            print('Connect from',addr)
        except KeyboardInterrupt:
            print('服务退出')
        except Exception as e:
            print(e)
            continue

        # 创建子进程
        p = Process(target=request,args=(c,))
        p.daemon = True
        p.start()

if __name__ == '__main__':
    main()





