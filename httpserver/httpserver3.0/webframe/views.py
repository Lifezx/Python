'''
views.py
编写各种请求的处理方案
'''

def show_time():
    import time
    return time.ctime()

def guonei():
    return '国内'

def guoji():
    return '国际'