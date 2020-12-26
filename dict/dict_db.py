'''
数据库处理操作
'''

import pymysql
import hashlib

# 对密码进行加密处理
def md5(password):
    salt = '#$%205$#' # 加盐处理
    hash = hashlib.md5(salt.encode()) # 生成加密对象
    hash.update(password.encode())
    return hash.hexdigest()


class User:
    def __init__(self,database):
        self.db = pymysql.connect(user='root', passwd='root',
                                  database=database, charset='utf8')


    # 创建游标对象
    def create_cursor(self):
        self.cur = self.db.cursor()

    def register(self,name,password):

        sql = "select * from user where name = %s"
        self.cur.execute(sql,[name])
        r = self.cur.fetchone()
        #    查找到说明用户存在
        if r:
            return False
        else:
            # 插入用户名和密码
            sql = "insert into  user (name,password) values (%s,%s)"
            password = md5(password)  # 加密处理
            try:
                self.cur.execute(sql, [name,password])
                self.db.commit()
            except:
                self.db.rollback()
            return True


    def login(self,name,password):
        sql = "select * from user where name = %s and password = %s"
        password = md5(password)  # 加密处理
        self.cur.execute(sql,[name,password])

        r = self.cur.fetchone()
        # 查找到则登陆成功
        if r:
            return True
        else:
            return False

    def seek_word(self,word,name):
        sql = "select mean from words where word = %s"
        self.cur.execute(sql,[word])
        r = self.cur.fetchone()
        # 查找到单词意思
        if r:
            return r[0]

    def insert_history(self,word,name):
        sql = "insert into history (name,word) values (%s,%s)"
        try:
            self.cur.execute(sql,[name,word])
            self.db.commit()
        except:
            self.db.rollback()


    def history(self,name):
        sql = "select name,word,time from history where name = %s order by time desc"
        self.cur.execute(sql,[name])
        r = self.cur.fetchmany(10)
        if r:
            return r
