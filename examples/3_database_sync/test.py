# -*- coding:utf-8 -*-

import pymysql


# 1.连接
conn = pymysql.connect(host='172.17.0.1', port=3306, user='root', password='681296', db='automl', charset='utf8')
print(conn)

exit(2)
# 2.创建游标
cursor = conn.cursor()

#注意%s需要加引号
sql = "select * from t1.userinfo where username='%s' and pwd='%s'" %(user, pwd)
print(sql)

# 3.执行sql语句
cursor.execute(sql)

result=cursor.execute(sql) #执行sql语句，返回sql查询成功的记录数目
print(result)

# 关闭连接，游标和连接都要关闭
cursor.close()
conn.close()

if result:
    print('登陆成功')
else:
    print('登录失败')