#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
@File:      JDConfig.py
@Author:    Jim.Dai.Cn
@Date:      2020/6/24 下午1:20
@Desc:         
"""


class JDConfig:
    kafka_bootstrap_server = '192.168.1.157:9092'
    kafka_topic_user_info = 'togg'
    kafka_topic_company_info = 'company_info'
    # kafka_group_id = 'group_id'
    kafka_group_id_info = 'group_id_info'
    mysql_server = '192.168.1.157'
    mysql_user = 'platform_policy_match_test'
    mysql_psw = '123456'
    mysql_db = 'platform_policy_match_test'
    mysql_table = {}
    mysql_table['user_info'] = 'user_info'  # 企业信息
    mysql_table['user_login'] = 'user_login'  # 登陆信息
    mysql_table['project_info'] = 't_project_info'  # 项目
    mysql_table['intellectual'] = 't_user_intellectual'  # 知识产权
    mysql_table['financial'] = 't_user_financial'  # 财务
    mysql_table['manag_user'] = 'manag_user'
    mysql_table['upms_organization'] = 'upms_organization'
    mysql_table['upms_user_organization'] = 'upms_user_organization'
    mysql_table['user_contact'] = 't_user_contact'  # 联系人信息
    # mysql_table_target_form_user = 't_target_form_user'  # 企业填入的动态表格

    oracle_server = '192.168.1.88:/orcl'
    oracle_user = 'wuxihuishan_yutiaoshi'
    oracle_psw = '123456'
    oracle_db = 'WUXIHUISHAN_YUTIAOSHI'
    oracle_table = {}
    oracle_table['user_info'] = 'USER_INFO'
    oracle_table['user_login'] = 'USER_LOGIN'
    oracle_table['field_value_user'] = 'T_FIELD_VALUE_USER'  # 企业填入的动态表格
    oracle_table['manag_user'] = 'MANAG_USER'  # 管理员表
    oracle_table['upms_organization'] = 'UPMS_ORGANIZATION'  # 组织
    oracle_table['upms_user_organization'] = 'UPMS_USER_ORGANIZATION'  # upms组织

    # company_sync_api = 'http://192.168.1.178:'  # 同步完成之后调用接口更新 政策匹配结果
