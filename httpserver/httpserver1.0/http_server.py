'''
编写一个http服务端程序
    如果浏览器的请求内容 /index
    响应码为 200 OK,将index.html内容作为响应内容

    如果浏览器的请求是其他的
    响应码为 404 Not Found 内容为‘Sorry..’
'''
from socket import *

# 处理客户端事件
def handle(connfd):
    # 获取http请求
    data = connfd.recv(4096).decode()
    request_line = data.split('\n')[0]
    info = request_line.split(' ')[1]
    if info == '/index':
        with open('index.html') as f:
            # 组织http响应格式
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += f.read()
    else:
        response = '''HTTP/1.1 404 Not Found
                    Content-Type:text/html

                    <h1>Sorry...</h1>
                    '''
    # 发送给浏览器
    connfd.send(response.encode())

# 搭建网络
def main():
    # tcp服务端
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) #端口立即重用
    s.bind(('127.0.0.1',8000))
    s.listen(5)

    while True:
        connfd,addr = s.accept()
        print('Connect From',addr)
        # 处理客户端请求
        handle(connfd)

main()

