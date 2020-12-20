'''
save_file.py
二进制文件存储示例
'''
import pymysql




# 连接数据库
db = pymysql.connect(user = 'root',passwd = 'root',database = 'stu',charset = 'utf8')

# 创建游标
cur = db.cursor()


# 存储图片
# with open('1.jpg','rb') as f:
#     data = f.read()
#
# sql = "insert into image (id,photo,comment) values (1,%s,%s)"
# cur.execute(sql,[data,'男神'])
# db.commit()

# 提取图片
sql = "select photo from image where comment = '男神'"
cur.execute(sql)
data = cur.fetchone()[0]
with open('2.jpg','wb') as f:
    f.write(data)


cur.close()
db.close()
