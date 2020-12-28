#!/usr/bin/env python3
'''
webframe.py
模拟网站的后端应用行为

从httpserver接收具体请求
根据请求进行逻辑处理和数据处理
将需要的数据反馈给httpserver
'''

from socket import *
import json
from settings import *
from multiprocessing import Process
import signal
from urls import *

class Application:
    def __init__(self):
        self.s = socket()
        self.s.bind(frame_address)
        self.s.setsockopt(SOL_SOCKET,SO_REUSEADDR,DEBUG)

    # 启动服务
    def start(self):
        self.s.listen(5)
        print('Listen the port',frame_port)
        while True:
            connfd,addr = self.s.accept()
            p = Process(target=self.handle,args=(connfd,))
            p.daemon = True
            p.start()

    # 处理具体数据
    def handle(self,connfd):
        request = connfd.recv(1024).decode()
        request = json.loads(request)# 请求字典
        # request -> {'method':'GET','info':'xxx'}
        if request['method'] == 'GET':
            if request['info'] == '/' or request['info'][-5:] == '.html':
                response = self.get_html(request['info'])
            else:
                response = self.get_data(request['info'])
        elif request['method'] == 'PORT':
            pass

        # 将结果返回给httpserver
        try:
            response = json.dumps(response)
        except:
            connfd.close()
        connfd.send(response.encode())
        connfd.close()

    # 返回html
    def get_html(self,info):
        if info == '/':
            filename = DIR + '/index.html'
        else:
            filename = DIR + info
        try:
            f = open(filename)
        except Exception:
            with open(DIR+'/404.html') as f:
                return {'status':'404','data':f.read()}
        else:
            return {'status': '200', 'data': f.read()}

    def get_data(self,info):
        for url,func in urls:
            if url == info:
                return {'status': '200', 'data': func()}
        return {'status': '200', 'data': 'sorry'}


if __name__ == '__main__':
    app = Application()
    app.start()