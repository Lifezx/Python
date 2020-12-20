'''
mysql.py
pymysql 操作数据库基本流程
'''


import pymysql

# 连接数据库
db = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = 'root',
    database = 'stu',
    charset = 'utf8'
)

# 获取游标(操作数据库,执行sql语句,得到执行结果)
cur = db.cursor()

# 执行语句
sql = "insert into interest values(2,'Enma','draw','C',14888,'xxx');"
cur.execute(sql)

# 提交到数据库
db.commit()

# 关闭游标和数据库
cur.close()
db.close()