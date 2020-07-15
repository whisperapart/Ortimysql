#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
@File:      JDMySQL.py
@Author:    Jim.Dai.Cn
@Date:      2020/6/24 下午1:27
@Desc:         
"""

import pymysql
from JDConfig import JDConfig as JDConfig


class JDCMySQL:
    def __init__(self):
        # 打开数据库连接
        self.db = pymysql.connect(JDConfig.mysql_server, JDConfig.mysql_user, JDConfig.mysql_psw, JDConfig.mysql_db)
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def c(self):
        # 关闭数据库连接
        self.db.close()

    def i(self, table_name, data):
        k = ",".join(data.keys())
        # t = list(data.values())
        v = ','.join('%s' % i for i in list(data.values()))
        # print(data)
        # xdata = data;
        # xdata.pop('id')
        # motherfucker = ''
        # for key, value in data.items():
        #     motherfucker += ('{key}={value},'.format(key=key, value=value))
        # motherfucker = motherfucker[0: len(motherfucker)-1]
        # print(motherfucker)

        # sql = "INSERT INTO %s (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s" % (JDConfig.mysql_table_user_info, k, v, motherfucker)
        sql = "REPLACE INTO %s (%s) VALUES (%s)" % (table_name, k, v)
        print("\n%s\n" % sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            # print('ID = %s insert or update done.' % data['id'])
            return 1
        except:
            self.db.rollback()
            f = open("./errlog.txt", "a")
            print('ID = %s insert or update fail.' % data['id'])
            print('ID = %s insert or update fail.\nsql=\n%s\ndata=%s\n' % (data['id'], sql, data), file=f)
            f.close()
            return 0

    def u(self, table_name, data):
        pass

    def d(self, table_name, data):
        sql = "DELETE FROM %s WHERE id=%s" % (table_name, int(data["id"]))
        try:
            self.cursor.execute(sql)
            self.db.commit()
            # print('ID = %s delete done.' % data['id'])
            return 1
        except:
            self.db.rollback()
            # print('ID = %s delete fail.\n sql = %s \n' % (data['id'], sql))
            return 0

    def q(self, table_name, rid):
        sql = "SELECT * FROM %s WHERE id=%s" % (table_name, rid)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        print(data)
        return data

    # get total record
    def len(self, table_name):
        sql = "SELECT COUNT('') AS length FROM %s" % table_name
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        return data['length']

    # get by page
    def p(self, table_name, start=0, p=100):
        sql = "SELECT * FROM %s order by id LIMIT %s,%s" % (table_name, start, p)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def t(self, table_name):
        sql = 'DELETE FROM %s' % table_name
        ret = 0
        try:
            ret = self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
        return ret
