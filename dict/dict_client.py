'''
在线词典 客户端

功能:发送请求 接受结果
'''

from socket import *
import sys,getpass

# 服务器地址
ADDR = ('127.0.0.1',8000)

s = socket()
s.connect(ADDR)
# 网络搭建,终端输入命令选项
def main():

    # 循环发起请求
    while True:
        print('\n=======一级界面=======')
        print('*****     login     *****')
        print('*****    register   *****')
        print('*****      exit   *****')
        print('========================')
        cmd = input('Command:')
        if cmd.strip() == 'login':
            do_login()
        elif cmd.strip() == 'register':
            do_register()
        elif cmd == 'exit':
            s.send(b'E')
            print('谢谢使用')
            break
        else:
            print('请输入正确命令!')

# 二级登录界面
def login(name):
    while True:
        print('\n=======%s 二级界面=======' %name)
        print('*****     seek_word     *****')
        print('*****      history   *****')
        print('*****      cancel   *****')
        print('========================')
        cmd = input('Command:')
        if cmd.strip() == 'seek_word':
            do_seek_word(name)
        elif cmd.strip() == 'history':
            do_history(name)
        elif cmd == 'cancel':
            return # 二级界面结束
        else:
            print('请输入正确命令!')

# 登录功能
def do_login():
    print('=====登陆界面=====')
    name = input('姓名:')
    password = getpass.getpass('密码:')
    s.send(('L '+name+' '+password).encode())
    data = s.recv(1024).decode()
    if data == 'ok':
        print('登陆成功')
        login(name)
    else:
        print('登陆失败')

# 注册功能
def do_register():
    while True:
        print('=====注册界面=====')
        name = input('姓名:')
        password = getpass.getpass('密码:')
        password1 = getpass.getpass('再次输入密码:')
        if password != password1:
            print('两次密码不一致')
            continue
        if (' ' in name) or (' ' in password):
            print('用户名或密码不能含有空格')
            continue
        s.send(('R '+name+' '+password).encode())
        data = s.recv(1024).decode()
        if data == 'ok':
            print('注册成功')
            do_login()
            return
        else:
            print('注册失败')

def do_seek_word(name):
    while True:
        print('=====查找单词=====')
        word = input('请输入需要查找的单词:')
        if not word:
            break
        s.send(('S '+word+' '+name).encode())
        data = s.recv(1024).decode()
        print(data)

def do_history(name):
    print('=====历史记录=====')
    s.send(('H ' +name).encode())
    while True:
        data = s.recv(1024).decode()
        if data == '##':
            break
        print(data)


if __name__ == '__main__':
    main()