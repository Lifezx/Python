'''
chat room 客户端
发送请求,展示结果
'''
from socket import *
import os,sys

# 服务器地址
ADDR = ('127.0.0.1',8888)


def do_send(s,name):
    while True:
        try:
            news = input('>>')
        except KeyboardInterrupt:
            news = 'q'
        if news.strip() == 'q':
            msg = 'Q '+name
            s.sendto(msg.encode(),ADDR)
            sys.exit('退出聊天室')
        msg = 'C %s %s'%(name,news)
        s.sendto(msg.encode(),ADDR)

def do_receive(s):
    while True:
        data,addr = s.recvfrom(4096)
        # 收到exit接收进程结束
        if data.decode() == 'EXIT':
            sys.exit()
        print(data.decode()+'\n>>',end='')

# 搭建网络
def main():
    s = socket(AF_INET,SOCK_DGRAM)
    # 进入聊天室
    while True:
        name = input('请输入您的昵称:')
        msg = 'L ' + name
        s.sendto(msg.encode(),ADDR)
        # 接收反馈
        data,addr = s.recvfrom(128)
        if data == b'OK':
            print('您已进入聊天室')
            break
        else:
            print(data.decode())

    # 进行聊天
    pid = os.fork()
    if pid < 0:
        sys.exit('Error!')
    elif pid == 0:
        do_receive(s)
    else:
        do_send(s,name)

    # 退出


if __name__ == '__main__':
    main()