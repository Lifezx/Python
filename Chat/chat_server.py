'''
chat room 服务端
'''

from socket import *
import os,sys

# 全局变量:很多封装模块都要用或者有特定含义
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)

# 存储用户
user = {}

# 处理用户登陆
def do_login(s,name,addr):
    if name in user or '管理员' in name:
        s.sendto('用户名存在'.encode(),addr)
        return
    else:
        s.sendto(b'OK',addr)
        # 先通知其他人
        msg = '\n%s加入群聊'%name
        for i in user:
            s.sendto(msg.encode(),user[i])
        # 加入字典
        user[name] = addr
# 处理消息收发
def do_chat(s,name,msg):
    news = '\n%s：%s'%(name,msg)
    for i in user:
        # 不发送自己
        if i != name:
            s.sendto(news.encode(),user[i])

# 退出
def do_quit(s,name):
    msg = '\n%s退出聊天室'%name
    for i in user:
        if i == name:
            s.sendto(b'EXIT',user[i])
        else:
            s.sendto(msg.encode(),user[i])
    del user[name] # 删除用户

# 循环获取客户端请求
def do_request(s):
    while True:
        data,addr = s.recvfrom(1024)
        x = data.decode().split(' ',2) # 只切前两项，防止后面消息中有空格
        # 根据不同的请求类型处理不同的事件
        if x[0] == 'L':
            do_login(s,x[1],addr)
        elif x[0] == 'C':
            do_chat(s,x[1],x[2])
        elif x[0] == 'Q':
            do_quit(s,x[1])

# 搭建网络
def main():
    # udp网络
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)
    pid = os.fork()
    if pid == 0:
        # 管理员消息处理
        while True:
            msg = input('管理员消息:')
            msg = 'C 管理员 ' +msg
            s.sendto(msg.encode(),ADDR)
    else:
        do_request(s) # 接收客户端请求

if __name__ == '__main__':
    main()
