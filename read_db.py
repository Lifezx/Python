'''
read_db.py
pymysql 读操作演示 （select）
'''

import pymysql

# 连接数据库
db = pymysql.connect(user = 'root',passwd = 'root',database = 'stu',charset = 'utf8')

# 创建游标
cur = db.cursor()

# 获取数据
sql = "select name,hobby from interest where hobby = 'draw';"
cur.execute(sql)

# 直接遍历游标
# for i in cur:
#     print(i)

#  获取所有查询结果
# all_row = cur.fetchall()
# print(all_row)

# 获取多个查询结果
# many_row = cur.fetchmany(1)
# print(many_row)

# 获取一个查询结果
one_row = cur.fetchone()
print(one_row)


cur.close()
db.close()