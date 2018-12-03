#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pymysql
import time

# 打开数据库连接
db = pymysql.connect("localhost","root","123","TESTDB" )

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

for i in range(50000):
    # SQL 插入语句
    sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
           LAST_NAME, AGE, SEX, INCOME) \
           VALUES ('%s', '%s', '%d', '%c', '%d' )" % \
           ('Mac', 'Mohan', 20, 'M', i)
    try:
        print(i)
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
        time.sleep(0.25)
    except:
        # 发生错误时回滚
        db.rollback()

db.close()
