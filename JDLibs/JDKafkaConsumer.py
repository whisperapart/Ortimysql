#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
@File:      JDKafkaConsumer.py
@Author:    Jim.Dai.Cn
@Date:      2020/6/24 下午1:28
@Desc:         
"""

import json
import threading

from kafka import KafkaConsumer, TopicPartition, OffsetAndMetadata
from JDLibs.JDConfig import JDConfig as JDConfig
from JDLibs.JDConvert import JDConvert as JDConvert
from JDLibs.JDKafkaProducer import Producer as Producer
from JDLibs.JDMySQL import JDCMySQL as JDCMySQL


def kafka_insert_thread(pn):
    if pn != '' and pn is not None:
        inserter = Producer('whatever')
        inserter.send_company_update_flag(pn)
        inserter.close()


def run_table(message, table_name, data):
    ret = 0
    my = JDCMySQL()
    switch = {
        "U": my.i,
        "I": my.i,
        # "D": my.d
    }
    try:
        op = message.value["op_type"]
        ret = switch[op](table_name, data)
    except KeyError as e:
        pass
    finally:
        my.c()
    return ret


def run_manag_user(message):
    d = message.value['after'] if message.value['op_type'] != 'D' else message.value['before']
    if isinstance(d, dict):
        d = json.dumps(d)
    d = json.loads(d)
    data = JDConvert.ogg2mysql_manag_user(d)
    ret = run_table(message, JDConfig.mysql_table['manag_user'], data)
    pn = data.get('paper_no', '')
    return ret, pn


def run_upms_org(message):
    d = message.value['after'] if message.value['op_type'] != 'D' else message.value['before']
    if isinstance(d, dict):
        d = json.dumps(d)
    d = json.loads(d)
    data = JDConvert.ogg2mysql_upms_org(d)
    ret = run_table(message, JDConfig.mysql_table['upms_organization'], data)
    pn = data.get('paper_no', '')
    return ret, pn


def run_upms_user_org(message):
    d = message.value['after'] if message.value['op_type'] != 'D' else message.value['before']
    if isinstance(d, dict):
        d = json.dumps(d)
    d = json.loads(d)
    data = JDConvert.ogg2mysql_upms_user_org(d)
    ret = run_table(message, JDConfig.mysql_table['upms_user_organization'], data)
    pn = data.get('paper_no', '')
    return ret, pn


def run_user_login(message):
    d = message.value['after'] if message.value['op_type'] != 'D' else message.value['before']
    if isinstance(d, dict):
        d = json.dumps(d)
    d = json.loads(d)
    data = JDConvert.ogg2mysql_user_login(d)
    ret = run_table(message, JDConfig.mysql_table['user_login'], data)
    pn = data.get('paper_no', '')
    return ret, pn


def run_user_field_value(message):
    ret = 0
    pn =''
    d = message.value['after'] if message.value['op_type'] != 'D' else message.value['before']
    if isinstance(d, dict):
        d = json.dumps(d)
    d = json.loads(d)

    fieldId = int(d['T_FIELD_NAME_ID'])
    # print("working field_id = %s " % fieldId)
    intercept = JDConvert.oracle_field_code_dispatcher(fieldId)
    tableName = ''
    if intercept is None:
        print('intercept catch, not in watch list, ignoring field_id = %s...' % fieldId)
        return ret, pn

    data = ''
    # print("==== converting \n")
    if intercept == 'financial':
        tableName = JDConfig.mysql_table['financial']
        data = JDConvert.ogg2mysql_financial(d)
    elif intercept == 'intellectual':
        tableName = JDConfig.mysql_table['intellectual']
        data = JDConvert.ogg2mysql_intellectual(d)
    elif intercept == 'project':
        tableName = JDConfig.mysql_table['project_info']
        data = JDConvert.ogg2mysql_project(d)
    # print("==== end of converting\n")

    if tableName == '':
        print('intercept catch, table name empty, ignoring...')
        return ret, pn

    ret = run_table(message, tableName, data)
    pn = data.get('paper_no', '')
    return ret, pn


def run_user_info(message):
    d = message.value['after'] if message.value['op_type'] != 'D' else message.value['before']
    if isinstance(d, dict):
        d = json.dumps(d)
    d = json.loads(d)
    data = JDConvert.ogg2mysql_user_info(d)
    ret = run_table(message, JDConfig.mysql_table['user_info'], data)
    pn = data.get('paper_no', '')
    if ret == 1:
        contArr = JDConvert.ogg2mysql_user_contact(d)
        for c in contArr:
            run_table(message, JDConfig.mysql_table['user_contact'], c)
    return ret, pn


class Consumer:
    def __init__(self, verbose, forceRestart=False):
        self.consumer = KafkaConsumer(bootstrap_servers=JDConfig.kafka_bootstrap_server,
                                      group_id=JDConfig.kafka_group_id_info,
                                      auto_offset_reset='earliest',
                                      value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                      consumer_timeout_ms=1000)
        self.topic_partition = TopicPartition(topic=JDConfig.kafka_topic_user_info, partition=0)
        self.consumer.assign([
            self.topic_partition,
        ]
        )
        committed_offset = None
        if not forceRestart:
            committed_offset = self.consumer.committed(self.topic_partition)
        if committed_offset is None:
            ##重置此消费者消费的起始位
            self.consumer.seek(partition=self.topic_partition, offset=0)
        self.verbose = verbose
        # debug purpose
        # self.consumer.seek(partition=self.topic_partition, offset=160768)

    def run(self):
        total = 0
        cnt = 0
        for message in self.consumer:
            total = total + 1
            pn = ''
            # user_info 基本照抄
            if message.value['table'] == JDConfig.oracle_db + '.' + JDConfig.oracle_table['user_info']:
                re, pn = run_user_info(message)
                cnt = cnt + re
                if self.verbose > 1:
                    print("total: %s / succ: %s" % (total, cnt))
            # user_login 完全照抄
            elif message.value['table'] == JDConfig.oracle_db + '.' + JDConfig.oracle_table['user_login']:
                re, pn = run_user_login(message)
                cnt = cnt + re
                if self.verbose > 0:
                    print("total: %s / succ: %s" % (total, cnt))
            # manag_user upms_organization upms_user_organization 完全照抄
            elif message.value['table'] == JDConfig.oracle_db + '.' + JDConfig.oracle_table['manag_user']:
                re, pn = run_manag_user(message)
                cnt = cnt + re
                if self.verbose > 0:
                    print("total: %s / succ: %s" % (total, cnt))
            elif message.value['table'] == JDConfig.oracle_db + '.' + JDConfig.oracle_table['upms_organization']:
                re, pn = run_upms_org(message)
                cnt = cnt + re
                if self.verbose > 0:
                    print("total: %s / succ: %s" % (total, cnt))
            elif message.value['table'] == JDConfig.oracle_db + '.' + JDConfig.oracle_table['upms_user_organization']:
                re, pn = run_upms_user_org(message)
                cnt = cnt + re
                if self.verbose > 0:
                    print("total: %s / succ: %s" % (total, cnt))
            # t_field_value_user 用户填写的字段的值，需要拦截[关注]的字段，填入mysql 对应的表格中
            elif message.value['table'] == JDConfig.oracle_db + '.' + JDConfig.oracle_table['field_value_user']:
                re, pn = run_user_field_value(message)
                cnt = cnt + re
                if self.verbose > 1:
                    print("total: %s / succ: %s" % (total, cnt))

            kafka_insert_thread(pn)

            self.consumer.commit(offsets={self.topic_partition: (OffsetAndMetadata(message.offset + 1, None))})
            committed_offset = self.consumer.committed(self.topic_partition)
            # if self.verbose > 1:
            print('o2m 已保存的偏移量:', committed_offset, end='\t')

    def close(self):
        self.consumer.close()
