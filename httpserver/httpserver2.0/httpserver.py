'''
httpserver2.0
env:python3.5
io多路复用 http练习
'''
from socket import *
from select import select

class HttpServer:
    def __init__(self,host = '0.0.0.0',port = 80,dir = None):
        self.host = host
        self.port = port
        self.dir = dir
        self.address = (host,port)
        # select 监控列表
        self.rlist = []
        self.wlist = []
        self.xlist = []
        self.create_socket()
        self.bind()

    # 启动服务
    def server_forever(self):
        self.sockfd.listen(5)
        print('Listen the port %d'%self.port)
        # 设置关注的io
        self.rlist.append(self.sockfd)
        while True:
            rs,ws,xs = select(self.rlist,self.wlist,self.xlist)
            for r in rs:
                if r is self.sockfd:
                    c,addr = r.accept()
                    self.rlist.append(c)
                else:
                    # 有客户端发请求
                    self.handle(r)

    # 处理客户端请求
    def handle(self,connfd):
        # 接收http请求
        request = connfd.recv(4096)
        # 客户端断开处理
        if not request:
            # 取消关注
            self.rlist.remove(connfd)
            connfd.close()
            return

        # 提取请求内容
        request_line = request.splitlines()[0]
        info = request_line.decode().split(' ')[1]
        print(info)

        # 将info情况分类
        if info == '/' or info [-5:] == '.html':
            self.get_html(connfd,info)
        else:
            self.get_data(connfd,info)

    def get_html(self,connfd,info):
        if info == '/':
            # 主页
            filename = self.dir + 'index.html'
        else:
            filename = self.dir +info

        try:
            f = open(filename,'r')
        except Exception:
            # 没有网页
            response = "HTTP/1.1 404 NOT Found\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += "<h1>Sorry</h1>"
        else:
            # 有网页
            response = "HTTP/1.1 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += f.read()
        finally:
            connfd.send(response.encode())

    def get_data(self,connfd,info):
        f = open(self.dir+'hello.jpg','rb')
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type:image/jpeg\r\n"
        response += "\r\n"
        response = response.encode()+f.read()
        connfd.send(response)

    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)

    # 绑定地址
    def bind(self):
        self.sockfd.bind(self.address)


if __name__ == '__main__':
    # 用户提供的内容
    HOST = '0.0.0.0'
    PORT = 8000
    DIR = './static/' # 网页目录

    http = HttpServer(HOST,PORT,DIR) # 实例化对象
    http.server_forever() # 启动服务