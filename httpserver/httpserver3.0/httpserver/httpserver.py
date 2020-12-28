#!/usr/bin/env python3

'''
httpserver3.0

获取http请求
解析http请求
将请求发送给WebFrame
从WebFrame接收反馈数据
将数据组织为Response格式发送给客户端
'''

from socket import *
import sys,signal
from threading import Thread
from config import *
import re
import json

# 和frame进行交互
def connect_frame(env):
    s = socket()
    try:
        # 连接webframe
        s.connect((frame_ip,frame_port))
    except:
        return
    data = json.dumps(env) # 转换为json
    s.send(data.encode()) # 发送请求
    data = s.recv(1024*1024*10).decode()
    try:
        return json.loads(data) # {'status':'200','data':'xxxx'}
    except:
        return

# 和浏览器交互
class Httpserver:
    def __init__(self):
        self.host = host
        self.port = port
        self.addr = (host,port)

        # 创建套接字
        self.create_socket()
        self.bind()

    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,DEBUG)
        signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    # 绑定地址
    def bind(self):
        self.sockfd.bind(self.addr)

    # 启动服务
    def serve_forever(self):
        self.sockfd.listen(5)
        print('Listen the port %d'%self.port)
        while True:
            connfd,addr = self.sockfd.accept()
            client = Thread(target=self.handle,args=(connfd,))
            client.setDaemon(True)
            client.start()

    # 具体处理客户端请求
    def handle(self,connfd):
        request = connfd.recv(4096).decode()
        pattern = r"(?P<method>[A-Z]+)\s+(?P<info>/\S*)"
        try:
            env = re.match(pattern,request).groupdict()
        except:
            connfd.close()
            return
        else:
            # 和frame进行交互
            response = connect_frame(env)
            if response:
                self.send_response(response,connfd)

    # 组织http响应,发送给浏览器
    def send_response(self,response,connfd):
        # response -> {'status':'200','data':'xxxx'}
        if response['status'] == '200':
            data = "HTTP/1.1 200 OK\r\n"
            data += "COntent-Type:text/html\r\n"
            data += '\r\n'
            data += response['data']
        elif response['status'] == '404':
            data = "HTTP/1.1 404 Not Found\r\n"
            data += "COntent-Type:text/html\r\n"
            data += '\r\n'
            data += response['data']
        connfd.send(data.encode())

if __name__ == '__main__':
    httpd = Httpserver()
    httpd.serve_forever() # 启动服务