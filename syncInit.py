#!/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/bin python
# # -*- coding: utf-8 -*-

"""
@File:      syncInit.py
@Author:    Jim.Dai.Cn
@Date:      2020/6/30 上午9:53
@Desc:      1. 清空mysql.user_info表
@Desc:      2. 把oracle 表的所有数据逐条构造成 op_type = "I" after={} 丢入队列
"""
import sys

from JDConfig import JDConfig as JDConfig
from JDLibs.JDKafkaProducer import Producer as Producer
from JDLibs.JDMySQL import JDCMySQL as JDCMySQL
from JDLibs.JDOracle import JDCOracle as oracle


def usage():
    print('Usage: python syncInit.py [option] <table_name>\n'
          '\t\033[0;32;40m forceDrop \033[0m\t\tForce to DROP MySQL Table\n'
          '\t\033[0;31;40m insertAll \033[0m\t\tInsert all rows from oracle to kafka\n'
          )


def main():
    if len(sys.argv) != 3:
        usage()
    else:
        opt = sys.argv[1]
        table_name = sys.argv[2]
        if opt == 'forceDrop':
            if ask_for_confirm('FBI WARNING!\r\n警告！继续执行将会清空MySQL数据，是否确定继续? \r\n(y/n)'):
                force_drop(table_name)
        elif opt == 'insertAll':
            insert_all(table_name)
        else:
            usage()


def ask_for_confirm(warning):
    confirm = input(warning)
    return True if confirm == 'y' else False


def force_drop(table_name):
    # connect to mysql and exec drop
    my = JDCMySQL()
    if table_name in JDConfig.mysql_table.values():
        t = my.t(table_name)
        print('[ %s ] : %s row(s) deleted.' % (table_name, t))
    else:
        print('[ %s ] : is not in table list.' % table_name)
    my.c()


def insert_all(table_name):
    ora = oracle()
    total = 0
    if table_name in JDConfig.oracle_table.values():
        total = ora.length(table_name)
        print("%s , TOTAL = %s" % (table_name, total))
    else:
        ora.c()
        print('[ %s ] : is not in table list.' % table_name)
        return

    inserter = Producer(table_name)
    for i in range(1, total + 1, 10):
        dic = ora.p(table_name, i, i + 10)
        inserter.run(dic)
    ora.c()
    inserter.close()


if __name__ == '__main__':
    main()
