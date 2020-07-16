#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
@File:      JDKafkaProducer.py
@Author:    Jim.Dai.Cn
@Date:      2020/6/30 下午1:13
@Desc:         
"""

import json
import time

from kafka import KafkaProducer
from kafka.errors import kafka_errors

from JDLibs.JDConfig import JDConfig as JDConfig


# Allows to pass date objects
class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):  # pylint: disable=method-hidden
        try:
            return super(DatetimeEncoder, obj).default(obj)
        except TypeError:
            return str(obj)


class Producer:
    def __init__(self, table_name):
        self.producer = KafkaProducer(bootstrap_servers=JDConfig.kafka_bootstrap_server)
        self.table_name = table_name

    def run(self, arr):
        msg_dict = {'table': JDConfig.oracle_db + '.' + self.table_name,
                    'op_type': 'I',
                    'op_ts': '',
                    'current_ts': '',
                    'primary_keys': ['ID'],
                    'before': {},
                    'after': ''
                    }
        for a in arr:
            msg_dict['after'] = json.dumps(a, cls=DatetimeEncoder)
            msg_dict['op_ts'] = time.strftime("%Y-%m-%d %H:%M:%S")
            msg_dict['current_ts'] = time.strftime("%Y-%m-%d %H:%M:%S")

            msg = json.dumps(msg_dict, cls=DatetimeEncoder).encode()
            # print("\r\n== insert to kafka: %s" % msg)
            future = self.producer.send(JDConfig.kafka_topic_user_info, msg)
            try:
                record_metadata = future.get(timeout=10)
                print(record_metadata.topic, end=" ")
                print(record_metadata.partition, end=" ")
                print(record_metadata.offset)
            except kafka_errors as e:
                print(str(e))

    def close(self):
        self.producer.close()
