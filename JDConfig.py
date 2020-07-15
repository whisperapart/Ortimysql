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
    mysql_server = '192.168.1.157'
    mysql_user = 'platform_policy_match'
    mysql_psw = '123456'
    mysql_db = 'platform_policy_match'
    mysql_table_user_info = 'user_info'  # 企业信息
    mysql_table_user_login = 'user_login'  # 登陆信息
    mysql_table_project_info = 't_project_info'  # 项目
    mysql_table_intellectual = 't_user_intellectual'  # 知识产权
    mysql_table_financial = 't_user_financial'  # 财务
    # mysql_table_target_form_user = 't_target_form_user'  # 企业填入的动态表格
    mysql_table_manag_user = 'manag_user'
    mysql_table_upms_organization = 'upms_organization'
    mysql_table_upms_user_organization = 'upms_user_organization'

    oracle_server = '192.168.1.88:/orcl'
    oracle_user = 'wuxihuishan_yutiaoshi'
    oracle_psw = '123456'
    oracle_db = 'WUXIHUISHAN_YUTIAOSHI'
    oracle_table_user_info = 'USER_INFO'
    oracle_table_user_login = 'USER_LOGIN'
    # oracle_table_project_info = 't_user_project_info'
    # oracle_table_intellectual = 't_user_intellectual'  # 知识产权
    # oracle_table_financial = 't_user_financial'  # 财务
    # oracle_table_target_form_user = 'T_TARGET_FORM_USER'  # 企业填入的动态表格
    oracle_table_field_value_user = 'T_FIELD_VALUE_USER'  # 企业填入的动态表格
    oracle_table_manag_user = 'MANAG_USER'  # 管理员表
    oracle_table_upms_organization = 'UPMS_ORGANIZATION'  # 组织
    oracle_table_upms_user_organization = 'UPMS_USER_ORGANIZATION'  # upms组织
