#!/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/bin python
# # -*- coding: utf-8 -*-

"""
@File:      JDOracle.py
@Author:    Jim.Dai.Cn
@Date:      2020/6/30 下午3:36
@Desc:         
"""
import json

import cx_Oracle
from JDConfig import JDConfig as JDConfig


# Allows to pass date objects
class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):  # pylint: disable=method-hidden
        try:
            return super(DatetimeEncoder, obj).default(obj)
        except TypeError:
            return str(obj)


def OutputTypeHandler(cursor, name, defaultType, size, precision, scale):
    if defaultType == cx_Oracle.CLOB:
        return cursor.var(cx_Oracle.LONG_STRING, arraysize=cursor.arraysize)
    elif defaultType == cx_Oracle.BLOB:
        return cursor.var(cx_Oracle.LONG_BINARY, arraysize=cursor.arraysize)


class JDCOracle:
    def __init__(self):
        # 打开数据库连接
        # os.environ["ORACLE_BASE"] = '/home/oracle/app'
        # os.environ["ORACLE_SID"] = 'xxx'
        # os.environ["ORACLE_HOME"] = '/opt/oracle/instantclient'
        # os.environ["DYLD_LIBRARY_PATH"] = '$ORACLE_HOME'
        # os.environ["LD_LIBRARY_PATH"] = '$ORACLE_HOME'
        # os.environ["NLS_LANG"] = "AMERICAN_AMERICA.UTF8"
        # os.environ["TNS_ADMIN"] = '$HOME/etc'
        # os.environ["PATH"] = '$PATH:$ORACLE_HOME'
        # print(os.environ)

        self.db = cx_Oracle.connect(JDConfig.oracle_user,
                                    JDConfig.oracle_psw,
                                    JDConfig.oracle_server
                                    )
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.db.outputtypehandler = OutputTypeHandler
        self.cursor = self.db.cursor()

    def c(self):
        # 关闭数据库连接
        self.db.close()

    def dynTableQuery(self, field_id, form_user_id):
        sql = '''
        select aa.*,i.ID as company_id, i.PAPER_NO_ABCDEF as paper_no, i.USER_NAME_ABCDEF as company_name from 
        (select t.ID,t.T_FIELD_NAME_ID,t.T_TARGET_ID,u.CODE,u.VALUE,u.T_TARGET_FORM_USER_ID,tb.USER_ID,
        u.UPDATE_TIME, u.CREATE_TIME,to_char(u.UPDATE_TIME,'yyyy') as fill_year 
            from T_TARGET_FIELD t
            join T_FIELD_VALUE_USER u on t.T_FIELD_NAME_ID = u.T_FIELD_NAME_ID
            join T_TARGET_FIELD c on c.T_TARGET_ID = t.T_TARGET_ID AND c.T_FIELD_NAME_ID=''' + str(field_id) + '''
            join T_TARGET_FORM_USER tb on tb.T_TARGET_ID=t.T_TARGET_ID and u.T_TARGET_FORM_USER_ID=tb.ID
            where u.T_TARGET_FORM_USER_ID=''' + str(form_user_id) + '''
        )aa 		
        join USER_INFO i on i.ID = aa.USER_ID
        '''
        # print("====\n%s\n" % sql)
        self.cursor.execute(sql)
        desc = [d[0] for d in self.cursor.description]
        result = [dict(zip(desc, line)) for line in self.cursor]
        return result

    def p(self, table, start, end):
        dbtable = JDConfig.oracle_db + "." + table
        sql = ' select * from %s where rownum<%s minus select * from %s where rownum<%s' % \
              (dbtable, end,
               dbtable, start)
        self.cursor.execute(sql)
        desc = [d[0] for d in self.cursor.description]
        result = [dict(zip(desc, line)) for line in self.cursor]
        return result

    def length(self, table_name):
        sql = ' select count(*) as length from %s' % \
              (JDConfig.oracle_db + "." + table_name)
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        return row[0]
