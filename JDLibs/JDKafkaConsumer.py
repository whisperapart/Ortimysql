#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
@File:      JDKafkaConsumer.py
@Author:    Jim.Dai.Cn
@Date:      2020/6/24 下午1:28
@Desc:         
"""

import json
from kafka import KafkaConsumer, TopicPartition, OffsetAndMetadata
from JDConfig import JDConfig as JDConfig
from JDLibs.JDConvert import JDConvert as JDConvert
from JDLibs.JDMySQL import JDCMySQL as JDCMySQL


class Consumer():
    def __init__(self, verbose, forceRestart=False):
        self.consumer = KafkaConsumer(bootstrap_servers=JDConfig.kafka_bootstrap_server,
                                      group_id='group_id',
                                      auto_offset_reset='earliest',
                                      value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                      consumer_timeout_ms=1000)
        # self.consumer.subscribe([JDConfig.kafka_topic_user_info])

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
        # end_offset = self.consumer.end_offsets([self.topic_partition])[self.topic_partition]
        # print('已保存的偏移量:', committed_offset, '最新偏移量:', end_offset)
        # print(consumer.beginning_offsets(consumer.assignment()))  # 获取当前消费者可消费的偏移量
        # consumer.seek(TopicPartition(topic='test', partition=0), 5)  # 重置偏移量，从第5个偏移量消费
        self.verbose = verbose

    def run(self):
        total = 0
        cnt = 0
        for message in self.consumer:
            total = total + 1
            # user_info 基本照抄
            if message.value['table'] == JDConfig.oracle_db + '.' + JDConfig.oracle_table_user_info:
                cnt = cnt + self.run_user_info(message)
                if self.verbose > 1:
                    print("total: %s / succ: %s" % (total, cnt))
            # user_login 完全照抄
            elif message.value['table'] == JDConfig.oracle_db + '.' + JDConfig.oracle_table_user_login:
                cnt = cnt + self.run_user_login(message)
                if self.verbose > 0:
                    print("total: %s / succ: %s" % (total, cnt))
            # manag_user upms_organization upms_user_organization 完全照抄
            elif message.value['table'] == JDConfig.oracle_db + '.' + JDConfig.oracle_table_manag_user:
                cnt = cnt + Consumer.run_manag_user(message)
                if self.verbose > 0:
                    print("total: %s / succ: %s" % (total, cnt))
            elif message.value['table'] == JDConfig.oracle_db + '.' + JDConfig.oracle_table_upms_organization:
                cnt = cnt + self.run_upms_org(message)
                if self.verbose > 0:
                    print("total: %s / succ: %s" % (total, cnt))
            elif message.value['table'] == JDConfig.oracle_db + '.' + JDConfig.oracle_table_upms_user_organization:
                cnt = cnt + self.run_upms_user_org(message)
                if self.verbose > 0:
                    print("total: %s / succ: %s" % (total, cnt))
            # t_field_value_user 用户填写的字段的值，需要拦截[关注]的字段，填入mysql 对应的表格中
            # 知识产权 1350 JDConvert.intelCode('mysql_col_name')
            # 财务数据 1390 - 年度报表
            # 项目信息 select * from T_FIELD_VALUE_USER where T_FIELD_NAME_ID = 11790
            elif message.value['table'] == JDConfig.oracle_db + '.' + JDConfig.oracle_table_field_value_user:
                cnt = cnt + self.run_user_field_value(message)
                if self.verbose > 1:
                    print("total: %s / succ: %s" % (total, cnt))

            self.consumer.commit(offsets={self.topic_partition: (OffsetAndMetadata(message.offset + 1, None))})
            committed_offset = self.consumer.committed(self.topic_partition)
            # if self.verbose > 1:
            print('o2m 已保存的偏移量:', committed_offset, end='\t')

    def close(self):
        self.consumer.close()

    def run_user_info(self, message):
        ret = 0
        my = JDCMySQL()
        #  ConsumerRecord(topic='togg', partition=0, offset=9, timestamp=1593410403986, timestamp_type=0, key=b'WUXIHUISHAN_YUTIAOSHI.USER_INFO', value={'table': 'WUXIHUISHAN_YUTIAOSHI.USER_INFO', 'op_type': 'U', 'op_ts': '2020-06-29 13:59:54.855524', 'current_ts': '2020-06-29T14:00:03.344000', 'pos': '00000000020000003026', 'primary_keys': ['ID'], 'before': {}, 'after': {'ID': 1096, 'USER_ID': 196, 'STATE': 50, 'THIS_ROLE': None, 'SYS_ID': '4501', 'USER_NAME_ABCDEF': '无锡盛力达科技股份有限公司x', 'USER_TYPE_ABCDEF': '11', 'AREA_ID_C_ABCDEF': '450102', 'AREA_ID_B_ABCDEF': '4501', 'AREA_ID_A_ABCDEF': '45', 'AREA_ID_ABCDEF': '450102009', 'PAPER_TYPE_ABCDEF': None, 'PAPER_NO_ABCDEF': '91320200785959333M', 'PAPER_VALIDITY_ABCDEF': None, 'BANK_OPEN_ABCDEF': None, 'BANK_ACCOUNT_ABCDEF': None, 'OPEN_NAME_ABCDEF': None, 'OPEN_NO_ABCDEF': None, 'CONTACTS_ABCDEF': '孙强', 'FIXED_TEL_ABCDEF': '0510-85183218', 'MOVE_TEL_ABCDEF': '13771550061', 'MAIL_ABCDEF': 'sqfmd2011@163.com', 'FAX_ABCDEF': None, 'ADDR_ABCDEF': '无锡市惠山经济开发区堰新东路1号', 'REGIST_TIME_ABCE': '2006-03-21 00:00:00.000000000', 'REGIST_CAPITAL_AC': 12800.0, 'WORKERS_NO_AC': 141, 'DEVELOP_NO_A': 27, 'IP_NO_AC': None, 'IP_SYS_NO_AC': None, 'MAIN_PRODUCT_A': '电镀黄铜生产线、D系列钢丝双捻机、水箱拉丝机\r\n', 'MAIN_MARKET_A': None, 'IS_ISO_A': '999', 'COMPANY_TYPE_A': 102, 'INDUSTRY_A': '30', 'NATURE_A': '999', 'PROJ_A': '999', 'IS_GAUGE': '1', 'IS_CONTINUE_HIGH': None, 'LEGAL_PERSON_C': None, 'PROVINCES_RECORD_C': None, 'IS_HQ_C': None, 'HQ_USER_NAME_C': None, 'HQ_ADDR_C': None, 'HQ_ZIP_CODE_C': None, 'HQ_REGIST_ADDR_C': None, 'HQ_LEGAL_PERSON_C': '张德刚', 'HQ_NO_C': None, 'HQ_REGIST_TIME_C': None, 'HQ_EMPLOYMENT_C': None, 'HQ_PRACTISING_AGENT_C': None, 'HQ_CONTACTS_C': None, 'HQ_TEL_C': None, 'AGENT_NO_C': None, 'LAW_NO_C': None, 'NATIONAL_START_C': None, 'PROVINCE_START_C': None, 'REGISTRATION_C': None, 'REGISTRATION_VALIDITY_C': None, 'CREATE_TIME': '2019-11-15 13:45:34.609000000', 'REMARK': None, 'SPARE1': None, 'SPARE2': None, 'SPARE3': None, 'IS_DELETE': 0, 'ISO_CREATE_TIME': None, 'BUSSINESS_TIME_START': None, 'BUSSINESS_TIME_END': None, 'REGISTER_PLACE': None, 'CHECK_DAY': None, 'REGISTER_STATUS': 1, 'TECHNOLOGY_FIELD': '804', 'INVESTMENT_MONEY': None, 'DEV_MASTER_NUM': 1, 'DEV_DOCTOR_NUM': 0, 'INDEPENTDENT_LEGAL_PERSON': 1, 'NATIONAL_ECONOMY_INDUSTRY': '34', 'COMPANY_ATTRIBUTE': '非大型央企', 'COMPANY_SCALE': '小型', 'COMPANY_PROFILE': None, 'COMPANY_CREDIT_RATING': 'AAA', 'IS_ON_LISTED': '1', 'COMPANY_LISTING_SECTOR': '5', 'LEGAL_PERSON_TEL': '13771550061', 'FINANCE_CONTACT': '冯丽丽', 'FINANCE_TEL': '0510-85183218-9001', 'FINANCE_MOBEL': '13852400908', 'FINANCE_EMAIL': None}}, headers=[], checksum=None, serialized_key_size=31, serialized_value_size=2419, serialized_header_size=-1)
        d = message.value['after'] if message.value['op_type'] != 'D' else message.value['before']
        if isinstance(d, dict):
            d = json.dumps(d)
        d = json.loads(d)
        data = JDConvert.ogg2mysql_user_info(d)
        switch = {
            "U": my.i,
            "I": my.i,
            "D": my.d
        }
        try:
            op = message.value["op_type"]
            ret = switch[op](JDConfig.mysql_table_user_info, data)
        except KeyError as e:
            pass
        finally:
            my.c()
        return ret

    def run_user_login(self, message):
        ret = 0
        my = JDCMySQL()
        #  ConsumerRecord(topic='togg', partition=0, offset=9, timestamp=1593410403986, timestamp_type=0, key=b'WUXIHUISHAN_YUTIAOSHI.USER_INFO', value={'table': 'WUXIHUISHAN_YUTIAOSHI.USER_INFO', 'op_type': 'U', 'op_ts': '2020-06-29 13:59:54.855524', 'current_ts': '2020-06-29T14:00:03.344000', 'pos': '00000000020000003026', 'primary_keys': ['ID'], 'before': {}, 'after': {'ID': 1096, 'USER_ID': 196, 'STATE': 50, 'THIS_ROLE': None, 'SYS_ID': '4501', 'USER_NAME_ABCDEF': '无锡盛力达科技股份有限公司x', 'USER_TYPE_ABCDEF': '11', 'AREA_ID_C_ABCDEF': '450102', 'AREA_ID_B_ABCDEF': '4501', 'AREA_ID_A_ABCDEF': '45', 'AREA_ID_ABCDEF': '450102009', 'PAPER_TYPE_ABCDEF': None, 'PAPER_NO_ABCDEF': '91320200785959333M', 'PAPER_VALIDITY_ABCDEF': None, 'BANK_OPEN_ABCDEF': None, 'BANK_ACCOUNT_ABCDEF': None, 'OPEN_NAME_ABCDEF': None, 'OPEN_NO_ABCDEF': None, 'CONTACTS_ABCDEF': '孙强', 'FIXED_TEL_ABCDEF': '0510-85183218', 'MOVE_TEL_ABCDEF': '13771550061', 'MAIL_ABCDEF': 'sqfmd2011@163.com', 'FAX_ABCDEF': None, 'ADDR_ABCDEF': '无锡市惠山经济开发区堰新东路1号', 'REGIST_TIME_ABCE': '2006-03-21 00:00:00.000000000', 'REGIST_CAPITAL_AC': 12800.0, 'WORKERS_NO_AC': 141, 'DEVELOP_NO_A': 27, 'IP_NO_AC': None, 'IP_SYS_NO_AC': None, 'MAIN_PRODUCT_A': '电镀黄铜生产线、D系列钢丝双捻机、水箱拉丝机\r\n', 'MAIN_MARKET_A': None, 'IS_ISO_A': '999', 'COMPANY_TYPE_A': 102, 'INDUSTRY_A': '30', 'NATURE_A': '999', 'PROJ_A': '999', 'IS_GAUGE': '1', 'IS_CONTINUE_HIGH': None, 'LEGAL_PERSON_C': None, 'PROVINCES_RECORD_C': None, 'IS_HQ_C': None, 'HQ_USER_NAME_C': None, 'HQ_ADDR_C': None, 'HQ_ZIP_CODE_C': None, 'HQ_REGIST_ADDR_C': None, 'HQ_LEGAL_PERSON_C': '张德刚', 'HQ_NO_C': None, 'HQ_REGIST_TIME_C': None, 'HQ_EMPLOYMENT_C': None, 'HQ_PRACTISING_AGENT_C': None, 'HQ_CONTACTS_C': None, 'HQ_TEL_C': None, 'AGENT_NO_C': None, 'LAW_NO_C': None, 'NATIONAL_START_C': None, 'PROVINCE_START_C': None, 'REGISTRATION_C': None, 'REGISTRATION_VALIDITY_C': None, 'CREATE_TIME': '2019-11-15 13:45:34.609000000', 'REMARK': None, 'SPARE1': None, 'SPARE2': None, 'SPARE3': None, 'IS_DELETE': 0, 'ISO_CREATE_TIME': None, 'BUSSINESS_TIME_START': None, 'BUSSINESS_TIME_END': None, 'REGISTER_PLACE': None, 'CHECK_DAY': None, 'REGISTER_STATUS': 1, 'TECHNOLOGY_FIELD': '804', 'INVESTMENT_MONEY': None, 'DEV_MASTER_NUM': 1, 'DEV_DOCTOR_NUM': 0, 'INDEPENTDENT_LEGAL_PERSON': 1, 'NATIONAL_ECONOMY_INDUSTRY': '34', 'COMPANY_ATTRIBUTE': '非大型央企', 'COMPANY_SCALE': '小型', 'COMPANY_PROFILE': None, 'COMPANY_CREDIT_RATING': 'AAA', 'IS_ON_LISTED': '1', 'COMPANY_LISTING_SECTOR': '5', 'LEGAL_PERSON_TEL': '13771550061', 'FINANCE_CONTACT': '冯丽丽', 'FINANCE_TEL': '0510-85183218-9001', 'FINANCE_MOBEL': '13852400908', 'FINANCE_EMAIL': None}}, headers=[], checksum=None, serialized_key_size=31, serialized_value_size=2419, serialized_header_size=-1)
        d = message.value['after'] if message.value['op_type'] != 'D' else message.value['before']
        if isinstance(d, dict):
            d = json.dumps(d)
        d = json.loads(d)
        data = JDConvert.ogg2mysql_user_login(d)
        switch = {
            "U": my.i,
            "I": my.i,
            "D": my.d
        }
        try:
            op = message.value["op_type"]
            ret = switch[op](JDConfig.mysql_table_user_login, data)
        except KeyError as e:
            pass
        finally:
            my.c()
        return ret

    @staticmethod
    def run_manag_user(message):
        d = message.value['after'] if message.value['op_type'] != 'D' else message.value['before']
        if isinstance(d, dict):
            d = json.dumps(d)
        d = json.loads(d)
        data = JDConvert.ogg2mysql_manag_user(d)
        return Consumer.run_table(message, JDConfig.mysql_table_manag_user, data)

    @staticmethod
    def run_upms_org(message):
        d = message.value['after'] if message.value['op_type'] != 'D' else message.value['before']
        if isinstance(d, dict):
            d = json.dumps(d)
        d = json.loads(d)
        data = JDConvert.ogg2mysql_upms_org(d)
        return Consumer.run_table(message, JDConfig.mysql_table_upms_organization, data)

    @staticmethod
    def run_upms_user_org(message):
        d = message.value['after'] if message.value['op_type'] != 'D' else message.value['before']
        if isinstance(d, dict):
            d = json.dumps(d)
        d = json.loads(d)
        data = JDConvert.ogg2mysql_upms_user_org(d)
        return Consumer.run_table(message, JDConfig.mysql_table_upms_user_organization, data)

    @staticmethod
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

    def run_user_form(self, message):
        ret = 0
        my = JDCMySQL()
        # {"ID":3675,"T_TARGET_ID":1190,"USER_ID":1086,"STATUS":1,
        # "SUBMIT_TIME":"2019-11-13 14:22:38","CREATE_TIME":"2019-11-13 14:22:38","UPDATE_TIME":"2019-11-13 14:22:39",
        # "THIS_ROLE_ID":null}
        d = message.value['after'] if message.value['op_type'] != 'D' else message.value['before']
        if isinstance(d, dict):
            d = json.dumps(d)
        d = json.loads(d)
        data = JDConvert.ogg2mysql_user_form(d)
        switch = {
            "U": my.i,
            "I": my.i,
            "D": my.d
        }
        try:
            op = message.value["op_type"]
            ret = switch[op](JDConfig.mysql_table_target_form_user, data)
        except KeyError as e:
            pass
        finally:
            my.c()
        return ret

    def run_user_field_value(self, message):
        ret = 0
        # {"ID":28699,"T_FIELD_NAME_ID":12133,"T_TARGET_FORM_USER_ID":3758,
        # "CODE":"hzdw","VALUE":"华中科技大学x","SORT":3,"CREATE_TIME":"2019-11-13 15:36:17","UPDATE_TIME":"2019-11-13 15:36:17","SAME_TIME_VALUE":null,"SAME_PERIOD":null,"YEAR_TOTAL":null,"SELECT_VALUE":null,"FIELD_TYPE":null}}
        # print(message)

        d = message.value['after'] if message.value['op_type'] != 'D' else message.value['before']
        if isinstance(d, dict):
            d = json.dumps(d)
        d = json.loads(d)

        fieldId = int(d['T_FIELD_NAME_ID'])
        print("working field_id = %s " % fieldId)
        intercept = JDConvert.oracle_field_code_dispatcher(fieldId)
        tableName = ''
        if intercept is None:
            print('intercept catch, not in watch list, ignoring...')
            return ret

        my = JDCMySQL()
        d = message.value['after'] if message.value['op_type'] != 'D' else message.value['before']
        if isinstance(d, dict):
            d = json.dumps(d)
        d = json.loads(d)
        data = ''

        # print("==== converting \n")
        if intercept == 'financial':
            tableName = JDConfig.mysql_table_financial
            data = JDConvert.ogg2mysql_financial(d)
        elif intercept == 'intellectual':
            tableName = JDConfig.mysql_table_intellectual
            data = JDConvert.ogg2mysql_intellectual(d)
        elif intercept == 'project':
            tableName = JDConfig.mysql_table_project_info
            data = JDConvert.ogg2mysql_project(d)
        # print("==== end of converting\n")
        # {'eff_patent_total': '67', 'inventive': '5', 'utility_model': '3', 'design_patent': None, 'pct': None, 'apply_total': '60', 'apply_inventive': '57', 'apply_utility_model': '3', 'apply_design_patent': None, 'mark_total': None, 'madrid_trademark': None, 'trademark_introduction': None, 'software_total': None, 'software_copyright': None, 'total_new_drug_certificate': None, 'total_ic_layout': None}

        if tableName == '':
            print('intercept catch, table name empty, ignoring...')
            return ret

        switch = {
            "U": my.i,
            "I": my.i
            # "D": my.d # do not acknowledge delete
        }
        try:
            op = message.value["op_type"]
            ret = switch[op](tableName, data)
        except KeyError as e:
            pass
        finally:
            my.c()
        return ret

    # def step(self):
    #     message = self.consumer.poll()
    #     if message is None:
    #         return
    #     print(message)
    #
    #     my = JDCMySQL()
    #     if message.value['table'] != 'WUXIHUISHAN_YUTIAOSHI.USER_INFO':
    #         return  # for now, take care of user_info only
    #     #  ConsumerRecord(topic='togg', partition=0, offset=9, timestamp=1593410403986, timestamp_type=0, key=b'WUXIHUISHAN_YUTIAOSHI.USER_INFO', value={'table': 'WUXIHUISHAN_YUTIAOSHI.USER_INFO', 'op_type': 'U', 'op_ts': '2020-06-29 13:59:54.855524', 'current_ts': '2020-06-29T14:00:03.344000', 'pos': '00000000020000003026', 'primary_keys': ['ID'], 'before': {}, 'after': {'ID': 1096, 'USER_ID': 196, 'STATE': 50, 'THIS_ROLE': None, 'SYS_ID': '4501', 'USER_NAME_ABCDEF': '无锡盛力达科技股份有限公司x', 'USER_TYPE_ABCDEF': '11', 'AREA_ID_C_ABCDEF': '450102', 'AREA_ID_B_ABCDEF': '4501', 'AREA_ID_A_ABCDEF': '45', 'AREA_ID_ABCDEF': '450102009', 'PAPER_TYPE_ABCDEF': None, 'PAPER_NO_ABCDEF': '91320200785959333M', 'PAPER_VALIDITY_ABCDEF': None, 'BANK_OPEN_ABCDEF': None, 'BANK_ACCOUNT_ABCDEF': None, 'OPEN_NAME_ABCDEF': None, 'OPEN_NO_ABCDEF': None, 'CONTACTS_ABCDEF': '孙强', 'FIXED_TEL_ABCDEF': '0510-85183218', 'MOVE_TEL_ABCDEF': '13771550061', 'MAIL_ABCDEF': 'sqfmd2011@163.com', 'FAX_ABCDEF': None, 'ADDR_ABCDEF': '无锡市惠山经济开发区堰新东路1号', 'REGIST_TIME_ABCE': '2006-03-21 00:00:00.000000000', 'REGIST_CAPITAL_AC': 12800.0, 'WORKERS_NO_AC': 141, 'DEVELOP_NO_A': 27, 'IP_NO_AC': None, 'IP_SYS_NO_AC': None, 'MAIN_PRODUCT_A': '电镀黄铜生产线、D系列钢丝双捻机、水箱拉丝机\r\n', 'MAIN_MARKET_A': None, 'IS_ISO_A': '999', 'COMPANY_TYPE_A': 102, 'INDUSTRY_A': '30', 'NATURE_A': '999', 'PROJ_A': '999', 'IS_GAUGE': '1', 'IS_CONTINUE_HIGH': None, 'LEGAL_PERSON_C': None, 'PROVINCES_RECORD_C': None, 'IS_HQ_C': None, 'HQ_USER_NAME_C': None, 'HQ_ADDR_C': None, 'HQ_ZIP_CODE_C': None, 'HQ_REGIST_ADDR_C': None, 'HQ_LEGAL_PERSON_C': '张德刚', 'HQ_NO_C': None, 'HQ_REGIST_TIME_C': None, 'HQ_EMPLOYMENT_C': None, 'HQ_PRACTISING_AGENT_C': None, 'HQ_CONTACTS_C': None, 'HQ_TEL_C': None, 'AGENT_NO_C': None, 'LAW_NO_C': None, 'NATIONAL_START_C': None, 'PROVINCE_START_C': None, 'REGISTRATION_C': None, 'REGISTRATION_VALIDITY_C': None, 'CREATE_TIME': '2019-11-15 13:45:34.609000000', 'REMARK': None, 'SPARE1': None, 'SPARE2': None, 'SPARE3': None, 'IS_DELETE': 0, 'ISO_CREATE_TIME': None, 'BUSSINESS_TIME_START': None, 'BUSSINESS_TIME_END': None, 'REGISTER_PLACE': None, 'CHECK_DAY': None, 'REGISTER_STATUS': 1, 'TECHNOLOGY_FIELD': '804', 'INVESTMENT_MONEY': None, 'DEV_MASTER_NUM': 1, 'DEV_DOCTOR_NUM': 0, 'INDEPENTDENT_LEGAL_PERSON': 1, 'NATIONAL_ECONOMY_INDUSTRY': '34', 'COMPANY_ATTRIBUTE': '非大型央企', 'COMPANY_SCALE': '小型', 'COMPANY_PROFILE': None, 'COMPANY_CREDIT_RATING': 'AAA', 'IS_ON_LISTED': '1', 'COMPANY_LISTING_SECTOR': '5', 'LEGAL_PERSON_TEL': '13771550061', 'FINANCE_CONTACT': '冯丽丽', 'FINANCE_TEL': '0510-85183218-9001', 'FINANCE_MOBEL': '13852400908', 'FINANCE_EMAIL': None}}, headers=[], checksum=None, serialized_key_size=31, serialized_value_size=2419, serialized_header_size=-1)
    #     d = message.value['after'] if message.value['op_type'] != 'D' else message.value['before']
    #     d = json.loads(d)
    #     data = JDConvert.ogg2mysql(d)
    #
    #     switch = {
    #         "U": my.i,
    #         "I": my.i,
    #         "D": my.d
    #     }
    #     try:
    #         op = message.value["op_type"]
    #         print(op)
    #     except KeyError as e:
    #         pass
    #     finally:
    #         my.c()
    #
    #     self.consumer.commit(offsets={self.topic_partition: (OffsetAndMetadata(message.offset + 1, None))})
    #     committed_offset = self.consumer.committed(self.topic_partition)
    #     print('已保存的偏移量:', committed_offset)
