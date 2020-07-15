#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
@File:      JDConvert.py
@Author:    Jim.Dai.Cn
@Date:      2020/6/24 下午3:32
@Desc:         
"""
from collections import defaultdict

from JDLibs.JDOracle import JDCOracle as JDCOracle

sys_area = {
    '45': '江苏省', '4501': '无锡市', '450102': '惠山区',
    '450102002': '惠山软件园', '450102003': '数字信息产业园', '450102004': '生命科技产业园',
    '450102005': '高端装备产业园', '450102006': '惠山工业转型集聚区', '450102007': '科创中心',
    '450102008': '科研院所企业', '450102009': '其他'
}

intellectual_code = {
    'inventive': 12391,  # 发明专利件（有效专利）
    'utility_model': 12392,  # 实用新型（有效专利）
    'design_patent': 12393,  # 外观专利（有效专利）
    'pct': 12394,  # pct发明专利件（有效专利）
    'eff_patent_total': 12390,  # 有效专利总量
    'madrid_trademark': 12400,  # 马德里商标
    'trademark_introduction': 12401,  # 国内商标
    'mark_total': 12399,  # 商标总量
    'apply_inventive': 12396,  # 发明专利件（申请专利）
    'apply_utility_model': 12397,  # 实用新型（申请专利）
    'apply_design_patent': 12398,  # 外观专利（申请专利）
    'apply_total': 12395,  # 申请专利总量
    'software_copyright': 12404,  # 软件著作权
    'software_total': 12402,  # 著作权总量
    'total_ic_layout': 12412,  # 集成电路布图总量
    'total_new_drug_certificate': 12410  # 新药证书总量
}

financial_code = {
    'year': 12615,  # 年度
    'operating_income': 12619,  # 主营业收入
    'net_margin': 12620,  # 净利润
    'revenue': 12621,  # 税收
    # 'technology_import_cost': 技术引进费用
    # 'equipment_investment': 设备资金投入
    # 'software_investment': 软硬件资金投入
    # 'research': 研发投入
    # 'user_id': 用户id
    'user_name': 12613,  # 用户名称
    # 'is_delete': 1删除 2未删除
    # 'create_time': , # 创建时间
    # 'update_time':
    'paper_no': 12614,  # 证件号码
    'total_income': 12617,  # 总收入
    'total_business_income': 12616,  # 营业总收入
    'high_product_income': 12618,  # 其中高品收入
    'net_assets': 12622  # 净资产
    # 'internal_dev_input':其中：境内研发投,
}

project_code = {
    'project_name': 11790,  # 成功申报的项目数据
    'year':11791 # 年份
}


class JDConvert:
    @staticmethod
    def areaCodeToName(code):
        return sys_area[code] if code in sys_area else sys_area['450102009']

    @staticmethod
    def ogg2mysql_user_info(ogg):
        # done: area_id a b c  in mysql 应该是具体名称， 不是编号
        xogg = defaultdict(lambda: 0)
        for key in ogg:
            xogg[key] = ogg[key] if ogg[key] is not None else 0
            # ogg[key] = ogg[key] if ogg[key] is not None else 0
        ogg = xogg

        # print(ogg)
        # todo: - 联系人对应其他表 mysql.t_user_contact

        my = {}
        my['id'] = int(ogg["ID"])  # ID
        my['user_id'] = ogg["USER_ID"]  # 用户id
        my['user_name'] = '\'%s\'' % ogg["USER_NAME_ABCDEF"]  # 用户名称
        my["user_type"] = '\'%s\'' % ogg["USER_TYPE_ABCDEF"]  # 用户类型
        my["paper_no"] = '\'%s\'' % ogg["PAPER_NO_ABCDEF"]  # 证件号码
        my["enterprise_nature"] = '\'%s\'' % ogg["COMPANY_TYPE_A"]  # 企业性质
        my["paper_type"] = 0 if ogg["PAPER_TYPE_ABCDEF"] is None else ogg["PAPER_TYPE_ABCDEF"]  # 证件类型
        my["area_id_c"] = '\'%s\'' % JDConvert.areaCodeToName(ogg["AREA_ID_C_ABCDEF"])  # 所属地区县
        my["area_id_b"] = '\'%s\'' % JDConvert.areaCodeToName(ogg["AREA_ID_B_ABCDEF"])  # 所属地区市
        my["area_id_a"] = '\'%s\'' % JDConvert.areaCodeToName(ogg["AREA_ID_A_ABCDEF"])  # 所属地区省
        my["area_id"] = '\'%s\'' % JDConvert.areaCodeToName(ogg["AREA_ID_ABCDEF"])  # 所属地区
        # if "INDEPENTDENT_LEGAL_PERSON" in ogg.keys():
        my["is_legal_person"] = '\'%s\'' % ogg["INDEPENTDENT_LEGAL_PERSON"]  # 是否独立法人
        my["legal_person"] = '\'%s\'' % ogg["LEGAL_PERSON_C"]  # 法人
        # my["legal_person_degree"] = ogg[""]     # 法人学历
        my["legal_person_phone"] = '\'%s\'' % ogg["LEGAL_PERSON_TEL"]  # 法人手机
        # my["regist_capital"] = 0 if ogg["REGIST_CAPITAL_AC"] is None else ogg["REGIST_CAPITAL_AC"]  # 注册资本
        my["regist_capital"] = ogg["REGIST_CAPITAL_AC"]  # 注册资本
        my["regist_time"] = '\'%s\'' % ogg["REGIST_TIME_ABCE"] if ogg["REGIST_TIME_ABCE"] != 0 else 0  # 注册时间
        my["register_status"] = '\'%s\'' % ogg["REGISTER_STATUS"]  # 登记状态
        my["addr"] = '\'%s\'' % ogg["ADDR_ABCDEF"]  # 通讯地址
        my["technology_field"] = '\'%s\'' % ogg["TECHNOLOGY_FIELD"]  # 技术领域
        my["national_economy_industry"] = '\'%s\'' % ogg["NATIONAL_ECONOMY_INDUSTRY"]  # 国民经济行业
        my["enterprise_attribute"] = '\'%s\'' % ogg["COMPANY_ATTRIBUTE"]  # 企业属性
        my["enterprise_scale"] = '\'%s\'' % ogg["COMPANY_SCALE"]  # 企业规模
        my["is_gauge"] = '\'%s\'' % ogg["IS_GAUGE"]  # 规上企业0否1是
        my["credit_rating"] = '\'%s\'' % ogg["COMPANY_CREDIT_RATING"]  # 资信等级
        my["is_listed"] = '\'%s\'' % ogg["IS_ON_LISTED"]  # 是否上市
        my["listing_sector"] = '\'%s\'' % ogg["COMPANY_LISTING_SECTOR"]  # 其中上市板块
        my["master_project"] = '\'%s\'' % ogg["MAIN_PRODUCT_A"]  # 主营业务及产品
        # my["market_guonei"] = ogg[""]           # 产品国内市场份额
        # my["market_guowai"] = ogg[""]           # 产品国外市场份额
        # my["sources"] = ogg[""]                 # 信息来源
        # my["core_technology_sources"] = ogg[""] # 核心技术来源
        my["enterprise_info"] = '\'%s\'' % ogg["COMPANY_PROFILE"]  # 企业介绍
        my["open_bank"] = '\'%s\'' % ogg["BANK_OPEN_ABCDEF"]  # 开户行
        my["open_bank_no"] = '\'%s\'' % ogg["BANK_ACCOUNT_ABCDEF"]  # 开户账号
        # my["tax_no"] = ogg[""]                      # 税务登记证号
        # my["enterprise_area"] = ogg[""]                 # 企业占地面积（平米）
        my["enterprise_project"] = '\'%s\'' % ogg["PROJ_A"]  # 企业在建项目情况
        # my["industry_university"] = ogg[""]                 # 产学研合作大学
        # my["os_sys_info"] = ogg[""]                 # 办公自动化系统（签核）oa
        # my["plm_sys_info"] = ogg[""]                # 生命周期管理系统plm
        # my["erp_sys_info"] = ogg[""]                # 供应链系统或erp系统
        # my["mes_sys_info"] = ogg[""]                # 生产管理系统mes
        # my["financial_sys_info"] = ogg[""]          # 财务系统
        # my["equipment_sys_info"] = ogg[""]          # 设备系统mm
        # my["other_sys_info"] = ogg[""]              # 其他信息化系统
        # my["last_year_information_investment"] = ogg[""]    # 上年度信息化投入
        # ? my["state"] = ogg["STATE"]                       # 审核状态 0草稿 1审核中 2审核不通过 3审核通过
        # ? my["this_role"] = ogg["THIS_ROLE"]                   # 当前审批角色
        # my["provincial_cloud_star"] = ogg[""]           # 省上云评定星级
        # my["enterprise_cloud_investment"] = ogg[""]         # 企业上云年投入
        my["create_time"] = '\'%s\'' % ogg["CREATE_TIME"] if ogg["CREATE_TIME"] != 0 else 0  # 创建时间
        # my["update_time"] = ogg[""]                     # 更新时间
        my["ent_members"] = 0 if ogg["WORKERS_NO_AC"] is None else ogg["WORKERS_NO_AC"]  # 企业人员数
        my["ent_devtors"] = 0 if ogg["DEVELOP_NO_A"] is None else ogg["DEVELOP_NO_A"]  # 研发人数
        my["ent_doctorates"] = 0 if ogg["DEV_DOCTOR_NUM"] is None else ogg["DEV_DOCTOR_NUM"]  # 博士人数
        my["ent_masters"] = 0 if ogg["DEV_MASTER_NUM"] is None else ogg["DEV_MASTER_NUM"]  # 硕士人数
        # my["ent_threeyear_talents"] = ogg[""]           # 近三年人才引进
        return my

    @staticmethod
    def mysql2ogg_user_Info(my):
        # {'ID': 1096, 'USER_ID': 196, 'STATE': 50, 'THIS_ROLE': None, 'SYS_ID': '4501', 'USER_NAME_ABCDEF': '无锡盛力达科技股份有限公司x', 'USER_TYPE_ABCDEF': '11', 'AREA_ID_C_ABCDEF': '450102', 'AREA_ID_B_ABCDEF': '4501', 'AREA_ID_A_ABCDEF': '45', 'AREA_ID_ABCDEF': '450102009', 'PAPER_TYPE_ABCDEF': None, 'PAPER_NO_ABCDEF': '91320200785959333M', 'PAPER_VALIDITY_ABCDEF': None, 'BANK_OPEN_ABCDEF': None, 'BANK_ACCOUNT_ABCDEF': None, 'OPEN_NAME_ABCDEF': None, 'OPEN_NO_ABCDEF': None, 'CONTACTS_ABCDEF': '孙强', 'FIXED_TEL_ABCDEF': '0510-85183218', 'MOVE_TEL_ABCDEF': '13771550061', 'MAIL_ABCDEF': 'sqfmd2011@163.com', 'FAX_ABCDEF': None, 'ADDR_ABCDEF': '无锡市惠山经济开发区堰新东路1号', 'REGIST_TIME_ABCE': '2006-03-21 00:00:00.000000000', 'REGIST_CAPITAL_AC': 12800.0, 'WORKERS_NO_AC': 141, 'DEVELOP_NO_A': 27, 'IP_NO_AC': None, 'IP_SYS_NO_AC': None, 'MAIN_PRODUCT_A': '电镀黄铜生产线、D系列钢丝双捻机、水箱拉丝机\r\n', 'MAIN_MARKET_A': None, 'IS_ISO_A': '999', 'COMPANY_TYPE_A': 102, 'INDUSTRY_A': '30', 'NATURE_A': '999', 'PROJ_A': '999', 'IS_GAUGE': '1', 'IS_CONTINUE_HIGH': None, 'LEGAL_PERSON_C': None, 'PROVINCES_RECORD_C': None, 'IS_HQ_C': None, 'HQ_USER_NAME_C': None, 'HQ_ADDR_C': None, 'HQ_ZIP_CODE_C': None, 'HQ_REGIST_ADDR_C': None, 'HQ_LEGAL_PERSON_C': '张德刚', 'HQ_NO_C': None, 'HQ_REGIST_TIME_C': None, 'HQ_EMPLOYMENT_C': None, 'HQ_PRACTISING_AGENT_C': None, 'HQ_CONTACTS_C': None, 'HQ_TEL_C': None, 'AGENT_NO_C': None, 'LAW_NO_C': None, 'NATIONAL_START_C': None, 'PROVINCE_START_C': None, 'REGISTRATION_C': None, 'REGISTRATION_VALIDITY_C': None, 'CREATE_TIME': '2019-11-15 13:45:34.609000000', 'REMARK': None, 'SPARE1': None, 'SPARE2': None, 'SPARE3': None, 'IS_DELETE': 0, 'ISO_CREATE_TIME': None, 'BUSSINESS_TIME_START': None, 'BUSSINESS_TIME_END': None, 'REGISTER_PLACE': None, 'CHECK_DAY': None, 'REGISTER_STATUS': 1, 'TECHNOLOGY_FIELD': '804', 'INVESTMENT_MONEY': None, 'DEV_MASTER_NUM': 1, 'DEV_DOCTOR_NUM': 0, 'INDEPENTDENT_LEGAL_PERSON': 1, 'NATIONAL_ECONOMY_INDUSTRY': '34', 'COMPANY_ATTRIBUTE': '非大型央企', 'COMPANY_SCALE': '小型', 'COMPANY_PROFILE': None, 'COMPANY_CREDIT_RATING': 'AAA', 'IS_ON_LISTED': '1', 'COMPANY_LISTING_SECTOR': '5', 'LEGAL_PERSON_TEL': '13771550061', 'FINANCE_CONTACT': '冯丽丽', 'FINANCE_TEL': '0510-85183218-9001', 'FINANCE_MOBEL': '13852400908', 'FINANCE_EMAIL': None}
        ogg = {}
        ogg.ID = my['id']
        ogg.USER_ID = my['user_id']
        ogg.user_name = my['user_name']
        # my["user_type"]
        # my["paper_no"]
        # my["enterprise_nature"]
        # my["paper_type"]
        # my["area_id_c"]
        # my["area_id_b"]
        # my["area_id_a"]
        # my["area_id"]
        # my["is_legal_person"]
        # my["legal_person"]
        # my["legal_person_degree"]
        # my["legal_person_phone"]
        # my["regist_capital"]
        # my["regist_time"]
        # my["register_status"]
        # my["addr"]
        # my["technology_field"]
        # my["national_economy_industry"]
        # my["enterprise_attribute"]
        # my["enterprise_scale"]
        # my["is_gauge"]
        # my["credit_rating"]
        # my["is_listed"]
        # my["listing_sector"]
        # my["master_project"]
        # my["market_guonei"]
        # my["market_guowai"]
        # my["sources"]
        # my["core_technology_sources"]
        # my["enterprise_info"]
        # my["open_bank"]
        # my["open_bank_no"]
        # my["tax_no"]
        # my["enterprise_area"]
        # my["enterprise_project"]
        # my["industry_university"]
        # my["os_sys_info"]
        # my["plm_sys_info"]
        # my["erp_sys_info"]
        # my["mes_sys_info"]
        # my["financial_sys_info"]
        # my["equipment_sys_info"]
        # my["other_sys_info"]
        # my["last_year_information_investment"]
        # my["state"]
        # my["this_role"]
        # my["provincial_cloud_star"]
        # my["enterprise_cloud_investment"]
        # my["create_time"]
        # my["update_time"]
        # my["ent_members"]
        # my["ent_devtors"]
        # my["ent_doctorates"]
        # my["ent_masters"]
        # my["ent_threeyear_talents"]
        pass

    @staticmethod
    def ogg2mysql_user_login(ogg):
        xogg = defaultdict(lambda: 0)
        for key in ogg:
            xogg[key] = ogg[key] if ogg[key] is not None else 0
        ogg = xogg
        # {"ID":12404,"USER_ID":"wxgqyykj","USER_PW":"619503AB20C5C846274D118E67329ABD","STATE":1,"IS_DELETE":0,
        # "BEF_SYS_ID":null,"BEF_LOGINTIME":"2020-03-26 16:16:36.372000000","THIS_LOGINTIME":"2020-03-26 16:17:03.189000000",
        # "BEF_IP":"222.191.220.254","THIS_IP":"222.191.220.254",
        # "CREATE_TIME":"2020-03-26 16:08:45.481000000",
        # "REMARK":null,"SPARE1":"1"}
        my = {}
        my['ID'] = int(ogg["ID"])  # ID bigint
        my['USER_ID'] = '\'%s\'' % ogg["USER_ID"]  # 用户id varchar 100
        my['USER_PW'] = '\'%s\'' % ogg["USER_PW"]  # 密码 varchar 50
        my['STATE'] = int(ogg["STATE"])  # 状态 0 禁用 1正常 2 暂停 int
        my['IS_DELETE'] = int(ogg['IS_DELETE'])  # 是否删除0正常 1删除 int
        my['BEF_SYS_ID'] = '\'%s\'' % ogg["BEF_SYS_ID"]  # 上次登陆系统 varchar 50
        my['BEF_LOGINTIME'] = '\'%s\'' % ogg["BEF_LOGINTIME"] if ogg["BEF_LOGINTIME"] != 0 else 0  # 上次登陆时间 datetime
        my['THIS_LOGINTIME'] = '\'%s\'' % ogg["THIS_LOGINTIME"] if ogg["THIS_LOGINTIME"] != 0 else 0  # 本次登陆时间 datetime
        my['BEF_IP'] = '\'%s\'' % ogg["BEF_IP"]  # 上次登陆IP varchar 50
        my['THIS_IP'] = '\'%s\'' % ogg["THIS_IP"]  # 本次登陆IP varchar 50
        my['REMARK'] = '\'%s\'' % ogg["REMARK"]  # 备注 varchar 100
        # my['paper_no'] = '\'%s\''  # 信用代码 varchar 50
        # my['is_master'] = '\'%s\''  # 是否主账号 tinyint 1
        # my['nick_name'] = '\'%s\''  # 用户中文姓名 varchar 20
        # my['company_name'] = '\'%s\''  # 企业名称 varchar 100
        my['create_time'] = '\'%s\'' % ogg["create_time"] if ogg["create_time"] != 0 else 0  # 创建时间 timestamp
        # my['update_time'] = '\'%s\'' % ogg["update_time"] if ogg["update_time"] != 0 else 0  # 更新时间 timestamp
        return my

    @staticmethod
    def ogg2mysql_manag_user(ogg):
        xogg = defaultdict(lambda: 0)
        for key in ogg:
            xogg[key] = ogg[key] if ogg[key] is not None else 0
        ogg = xogg
        my = {}
        my['ID'] = int(ogg['ID'])    # ID bigint 20
        my['SYS_ID'] = '\'%s\'' % ogg['SYS_ID']  # 系统地区ID varchar 50
        my['MANAG_ID'] = '\'%s\'' % ogg['MANAG_ID']  # varchar 100
        my['MANAG_PW'] = '\'%s\'' % ogg['MANAG_PW']  # varchar 255
        my['STATE'] = int(ogg['STATE'])  # smallint 2
        my['IS_DELETE'] = int(ogg['IS_DELETE'])  # smallint 2
        my['BEF_SYS_ID'] = '\'%s\'' % ogg['BEF_SYS_ID']  # varchar 50
        my['BEF_LOGINTIME'] = '\'%s\'' % ogg["BEF_LOGINTIME"] if ogg["BEF_LOGINTIME"] != 0 else 0 # datetime
        my['THIS_LOGINTIME'] = '\'%s\'' % ogg["THIS_LOGINTIME"] if ogg["THIS_LOGINTIME"] != 0 else 0  # datetime
        my['BEF_IP'] = '\'%s\'' % ogg['BEF_IP']  # varchar 50
        my['THIS_IP'] = '\'%s\'' % ogg['THIS_IP']  # varchar 50
        my['MANAG_NAME'] = '\'%s\'' % ogg['MANAG_NAME']  # varchar 100
        my['TURE_NAME'] = '\'%s\'' % ogg['TURE_NAME']  # varchar 100
        my['TEL_PHONE'] = '\'%s\'' % ogg['TEL_PHONE']  # varchar 20
        # my['AREA_ID_C'] = ogg['']  # varchar 50
        # my['AREA_ID_B'] = ogg['']  # varchar 50
        # my['AREA_ID_A'] = ogg['']  # varchar 50
        # my['IS_AREA_ID'] = ogg['']  # varchar 50
        my['REMARK'] = '\'%s\'' % ogg['REMARK']  # varchar 100
        my['CREATE_TIME'] = '\'%s\'' % ogg["CREATE_TIME"] if ogg["CREATE_TIME"] != 0 else 0  # datetime

        return my

    @staticmethod
    def ogg2mysql_upms_org(ogg):
        xogg = defaultdict(lambda: 0)
        for key in ogg:
            xogg[key] = ogg[key] if ogg[key] is not None else 0
        ogg = xogg
        my = {}
        my['ID'] = int(ogg['ID'])  # ID bigint 20
        my['PID'] = int(ogg['PID'])  # PID bigint 20
        my['NAME'] = '\'%s\'' % ogg['NAME']  # varchar 20
        my['DESCRIPTION'] = '\'%s\'' % ogg['DESCRIPTION']  # varchar 2000
        my['leader_id'] = int(ogg['FGLD_USER_ID'])  # bigint 20
        my['leader_name'] = '\'%s\'' % ogg['FGLD_NAME']  # varchar 20
        # my['is_sub_company'] = int(ogg[''])  # int 2
        # my['is_del'] = int(ogg[''])  # int 2
        my['create_time'] = '\'%s\'' % ogg["CTIME"] if ogg["CTIME"] != 0 else 0 # timestamp
        # my['update_time'] = '\'%s\'' % ogg["CREATE_TIME"] if ogg["CREATE_TIME"] != 0 else 0  # timestamp
        # my['sort'] = int(ogg[''])  # smallint4
        return my

    @staticmethod
    def ogg2mysql_upms_user_org(ogg):
        xogg = defaultdict(lambda: 0)
        for key in ogg:
            xogg[key] = ogg[key] if ogg[key] is not None else 0
        ogg = xogg
        my = {'ID': int(ogg['ID']), 'USER_ID': int(ogg['USER_ID']), 'ORGANIZATION_ID': int(ogg['ORGANIZATION_ID'])}
        return my

    @staticmethod
    def ogg2mysql_user_form(ogg):
        xogg = defaultdict(lambda: 0)
        for key in ogg:
            xogg[key] = ogg[key] if ogg[key] is not None else 0
        ogg = xogg
        # {"ID":3675,"T_TARGET_ID":1190,"USER_ID":1086,"STATUS":1,
        # "SUBMIT_TIME":"2019-11-13 14:22:38","CREATE_TIME":"2019-11-13 14:22:38","UPDATE_TIME":"2019-11-13 14:22:39",
        # "THIS_ROLE_ID":null}
        my = {}
        my['ID'] = int(ogg["ID"])  # ID bigint
        my['T_TARGET_ID'] = int(ogg["T_TARGET_ID"])  # 指标表ID  bigint
        my['USER_ID'] = int(ogg["USER_ID"])  # 用户ID bigint
        my['STATUS'] = int(ogg["STATUS"])  # 状态 0 草稿 1提交 bigint
        my['SUBMIT_TIME'] = '\'%s\'' % ogg["SUBMIT_TIME"] if ogg["SUBMIT_TIME"] != 0 else 0  # 填报时间 datetime
        my['CREATE_TIME'] = '\'%s\'' % ogg["CREATE_TIME"] if ogg["CREATE_TIME"] != 0 else 0  # 创建时间 datetime
        my['UPDATE_TIME'] = '\'%s\'' % ogg["UPDATE_TIME"] if ogg["UPDATE_TIME"] != 0 else 0  # 更新时间 datetime

        return my

    @staticmethod
    def ogg2mysql_project(ogg):
        orc = JDCOracle()
        ret = orc.dynTableQuery(ogg['T_FIELD_NAME_ID'], ogg['T_TARGET_FORM_USER_ID'])
        orc.c()
        print(ret)
        my = {}
        for d in ret:
            k = JDConvert.my_project_col_from_oracle_code(d['T_FIELD_NAME_ID'])
            if k is not None:
                if d['VALUE'] is not None:
                    my[k] = '\'%s\'' % d['VALUE']
                    my['customer_id'] = d['COMPANY_ID']
                    my['paper_no'] = '\'%s\'' % d['PAPER_NO']
                    my['customer_name'] = '\'%s\'' % d['COMPANY_NAME']
                    my['id'] = d['T_TARGET_FORM_USER_ID']
                    x = int(d['FILL_YEAR'])
                    y = x - 1 if x > 0 else 0
                    my['year'] = '\'%s\'' % y
            # 项目表中的 year 字段
            if k == 'year' and d['VALUE'] is not None:
                my['year'] = d['VALUE']
        print("\n\n==>\n")
        print(my)
        return my

    @staticmethod
    def ogg2mysql_financial(ogg):
        orc = JDCOracle()
        ret = orc.dynTableQuery(ogg['T_FIELD_NAME_ID'], ogg['T_TARGET_FORM_USER_ID'])
        orc.c()
        print(ret)
        my = {}
        for d in ret:
            k = JDConvert.my_financial_col_from_oracle_code(d['T_FIELD_NAME_ID'])
            if k is not None:
                if d['VALUE'] is not None:
                    my[k] = d['VALUE']
                    # 这里处理得不优雅，不过懒得改了
                    my['user_id'] = d['COMPANY_ID']
                    my['paper_no'] = '\'%s\'' % d['PAPER_NO']
                    my['user_name'] = '\'%s\'' % d['COMPANY_NAME']
                    my['id'] = d['T_TARGET_FORM_USER_ID']
                    # year 的处理， 默认值
                    x = int(d['FILL_YEAR'])
                    y = x - 1 if x > 0 else 0
                    my['year'] = '\'%s\'' % y
                    # update time
                    my['update_time'] = '\'%s\'' % d['UPDATE_TIME'] if '\'%s\'' % d['UPDATE_TIME'] != 0 else 0
                    my['create_time'] = '\'%s\'' % d['CREATE_TIME'] if '\'%s\'' % d['CREATE_TIME'] != 0 else 0
            # 财务表中的 year 字段
            if k == 'year' and d['VALUE'] is not None:
                my['year'] = d['VALUE']
            # 解决mysql 逻辑删除问题
            my['is_delete'] = 2
        print("\n\n==>\n")
        print(my)
        return my

    @staticmethod
    def ogg2mysql_intellectual(ogg):
        orc = JDCOracle()
        ret = orc.dynTableQuery(ogg['T_FIELD_NAME_ID'], ogg['T_TARGET_FORM_USER_ID'])
        orc.c()
        print(ret)
        my = {}
        for d in ret:
            k = JDConvert.my_intellectual_col_from_oracle_code(d['T_FIELD_NAME_ID'])
            if k is not None:
                if d['VALUE'] is not None:
                    my[k] = d['VALUE']
                    # 这里处理得不优雅，不过懒得改了
                    my['user_id'] = d['COMPANY_ID']
                    my['paper_no'] = '\'%s\'' % d['PAPER_NO']
                    my['user_name'] = '\'%s\'' % d['COMPANY_NAME']
                    my['id'] = d['T_TARGET_FORM_USER_ID']
                    x = int(d['FILL_YEAR'])
                    y = x - 1 if x > 0 else 0
                    my['year'] = '\'%s\'' % y
                    # todo update-time create-time 暂不处理
        print("\n\n==>\n")
        print(my)
        return my

    @staticmethod
    def intelCode(myCode):
        '''
SELECT * from T_TARGET_FIELD f
JOIN T_FIELD_NAME n
on
f.T_FIELD_NAME_ID = n.ID
where f.T_TARGET_ID=1350

ID	T_FIELD_NAME_ID	T_FIELD_VALUE_ID	T_TARGET_ID	CREATE_TIME	PLAN_VALUE	ID(1)	NAME	CODE	SORT	FIELD_TYPE	GROUP_ID	SEARCH	MUST	FIELD_RULE	FIELD_LENGTH	CREATE_TIME(1)	UPDATE_TIME	VALUE_TYPE	FIELD_DW	FIELD_RULE_MESSAGE	FIELD_URL	FIELD_FORM_ID
20394	12404		1350	2019-10-24 16:12:41		12404	其中：软件著作权量	rjzpzzql	15	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:12:41	2019-10-24 16:12:50	integer
20380	12390		1350	2019-10-24 16:05:33		12390	有效专利总量	yxzlzl	1	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:05:33	2019-10-24 16:08:56	integer
20383	12393		1350	2019-10-24 16:07:43		12393	其中：有效外观专利量	wgzlsqj	4	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:07:43	2020-05-21 16:51:34	integer
20386	12396		1350	2019-10-24 16:09:51		12396	其中：发明专利申请量	fmzlssll	7	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:09:51	2019-10-24 16:09:51	integer
20389	12399		1350	2019-10-24 16:10:28		12399	申请商标总量	sqsbzl	10	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:10:28	2019-10-24 16:10:28	integer
20381	12391		1350	2019-10-24 16:06:21		12391	其中：有效发明专利量	fmzlsql	2	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:06:21	2020-05-21 16:51:18	integer
20382	12392		1350	2019-10-24 16:07:18		12392	其中：有效实用新型量	syxxsqa	3	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:07:18	2020-05-21 16:51:26	integer
20384	12394		1350	2019-10-24 16:08:10		12394	其中：有效PCT境外发明专利量	pctjwfm	5	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:08:10	2020-05-21 16:51:58	integer
20385	12395		1350	2019-10-24 16:08:49		12395	申请专利总量	sqzlzll	6	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:08:49	2019-10-24 16:09:13	integer
20387	12397		1350	2019-10-24 16:10:03		12397	其中：实用新型申请量	syxxsqlfde	8	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:10:03	2019-10-24 16:10:53	integer
20388	12398		1350	2019-10-24 16:10:12		12398	其中：外观专利申请量	wgzlsse	9	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:10:12	2019-10-24 16:10:39	integer
20390	12400		1350	2019-10-24 16:11:23		12400	其中：马德里商标申请量	mdlsbsql	11	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:11:23	2019-10-24 16:11:23	integer
20391	12401		1350	2019-10-24 16:11:37		12401	其中：国内商标申请量	gnlsbsql	12	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:11:37	2019-10-24 16:11:45	integer
20392	12402		1350	2019-10-24 16:12:07		12402	有效著作权总量	uydqzfel	13	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:12:07	2019-10-24 16:12:07	integer
20393	12403		1350	2019-10-24 16:12:29		12403	其中：作品著作权量	zpzzql	14	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:12:29	2020-06-02 14:51:55	integer	39
20395	12405		1350	2019-10-24 16:13:14		12405	申请著作权总量	sqzzqzlt	16	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:13:14	2019-10-24 16:13:14	integer
20396	12406		1350	2019-10-24 16:13:57		12406	其中：申请阶段作品著作权量	sqjdzpzz	17	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:13:57	2019-10-24 16:13:57	integer
20397	12407		1350	2019-10-24 16:14:15		12407	其中：申请阶段软件著作权量	sqjdzpzzrj	18	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:14:15	2019-10-24 16:14:15	integer
20398	12408		1350	2019-10-24 16:14:56		12408	已公开论文(篇)	lwygkfb	19	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:14:56	2020-06-02 14:29:46	integer
20399	12409		1350	2019-10-24 16:15:22		12409	已公开发表学术报告(篇)	xsbgygk	20	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:15:22	2020-06-02 14:29:40	integer
20400	12410		1350	2019-10-24 16:15:50		12410	新药证书(项)	xyzsyy	21	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:15:50	2020-06-02 14:29:32	integer
20401	12411		1350	2019-10-24 16:16:09		12411	医疗器械注册证(项)	ylqxzczz	22	text	121	1	0	rangelength="0,15"		2019-10-24 16:16:09	2020-06-02 14:29:26	keyword
20402	12412		1350	2019-10-24 16:16:41		12412	集成电路布图(件)	jcdlbt	23	text	121	1	0	rangelength="0,15" digits="true"		2019-10-24 16:16:41	2020-06-02 14:29:20	integer
        :return:
        '''
        return intellectual_code[myCode] if myCode in intellectual_code else 0

    '''
    ID	T_FIELD_NAME_ID	T_FIELD_VALUE_ID	T_TARGET_ID	CREATE_TIME	PLAN_VALUE	ID(1)	NAME	CODE	SORT	FIELD_TYPE	GROUP_ID	SEARCH	MUST	FIELD_RULE	FIELD_LENGTH	CREATE_TIME(1)	UPDATE_TIME	VALUE_TYPE	FIELD_DW	FIELD_RULE_MESSAGE	FIELD_URL	FIELD_FORM_ID
    20606	12616		1390	2020-05-12 13:33:38		12616	总产值	zcz	4	text	128		0	rangelength="0,15" number="true"		2020-05-12 13:33:38	2020-05-29 17:22:55	double
    20608	12618		1390	2020-05-12 13:36:20		12618	其中：主营业务收入	zyywsr	6	text	128		0	rangelength="0,15" number="true"		2020-05-12 13:36:20	2020-05-29 17:23:06	double
    20609	12619		1390	2020-05-12 13:37:11		12619	营业利润	lrze	7	text	128		0	rangelength="0,15" number="true"		2020-05-12 13:37:11	2020-05-29 17:23:10	double
    20610	12620		1390	2020-05-12 13:37:38		12620	净利润	jlr	8	text	128		0	rangelength="0,15" number="true"		2020-05-12 13:37:38	2020-05-29 17:23:13	double
    20611	12621		1390	2020-05-12 13:38:42		12621	实际上缴税费总额	ss	9	text	128		0	rangelength="0,15" number="true"		2020-05-12 13:38:42	2020-05-29 17:23:20	double
    20607	12617		1390	2020-05-12 13:35:18		12617	营业收入	zsr	5	text	128		0	rangelength="0,15" number="true"		2020-05-12 13:35:18	2020-05-29 17:23:01	double
    20612	12622		1390	2020-05-12 13:39:21		12622	年末资产总计	zcze	10	text	128		0	rangelength="0,15" number="true"		2020-05-12 13:39:21	2020-05-29 17:23:27	double
    20613	12623		1390	2020-05-12 13:39:58		12623	年末负债合计	fzhj	11	text	128		0	rangelength="0,15" number="true"		2020-05-12 13:39:58	2020-05-29 17:23:32	double
    20614	12624		1390	2020-05-12 13:42:06		12624	当年获得创业风险投资机构的风险投资额	dnfxtze	12	text	129		0	rangelength="0,15" number="true"		2020-05-12 13:42:06	2020-05-29 17:23:35	double
    20615	12625		1390	2020-05-12 13:42:37		12625	累计获得创业风险投资机构的风险投资额	ljfxtze	13	text	129		0	rangelength="0,15" number="true"		2020-05-12 13:42:37	2020-05-29 17:23:38	double
    20603	12613		1390	2020-05-12 13:14:14		12613	企业名称	qymc	3	text	126		0	rangelength="0,100"  readonly="readonly"  alt="readonly"		2020-05-12 13:14:14	2020-05-18 12:02:31
    20604	12614		1390	2020-05-12 13:23:29		12614	统一社会信用代码	tyshxydm	2	text	126		0	readonly="readonly"  alt="readonly"		2020-05-12 13:23:29	2020-05-18 12:03:16
    20605	12615		1390	2020-05-12 13:25:08		12615	年度	nd	1	dateYear	126		1	required="true"  isYear="Y"		2020-05-12 13:25:08	2020-05-18 12:03:06				/sysconfig/selectOption.cy?pageSize=100&type=10013
    '''

    @staticmethod
    def finCode(myCode):
        return financial_code[myCode] if myCode in financial_code else 0

    '''
    ID	T_FIELD_NAME_ID	CODE	VALUE	SORT	T_TARGET_FORM_USER_ID	CREATE_TIME	UPDATE_TIME	SAME_TIME_VALUE	SAME_PERIOD	YEAR_TOTAL	SELECT_VALUE	FIELD_TYPE
    28624	11790	ryzz	无锡市雏鹰企业	2	3748	2019-11-13 15:33:38	2019-11-13 15:33:38					
    28716	11790	ryzz	国家科技型中小企业信息库入库企业	2	3762	2019-11-13 15:38:38	2019-11-13 15:38:38					
    '''

    # select * from T_FIELD_VALUE_USER where T_FIELD_NAME_ID = 11790
    @staticmethod
    def projectCode(myCode):
        oracle_code = {
            # 'year': ,#  年份
            # 'level': ,# 级别
            # 'window': ,# 条口
            # 'project_name': 'VALUE', # 项目名称
            # 'projec_name_id': ,# 项目名称表id
            'state': 2,  # 1进行汇总 2立项通过 3立项未通过
            'source': 1,  # 1来自系统 2管理部添加
            # 'customer_id': 'T_TARGET_FORM_USER_ID',# 客户id
            # 'custoer_name': ,# 客户名称
            # 'create_by': ,# 创建人id
            # 'create_name': ,# 创建人名称
            # 'create_date': ,# 创建时间 NOT null
            # 'update_date': ,# 更新时间 NOT NULL
            # 'project_type': ,# 项目类型
            # 'paper_no': ,# 证件号码
            # 'capital_limit': ,# 争取资金额度
        }
        return oracle_code[myCode] if myCode in oracle_code else 0

    @staticmethod
    def oracle_field_code_dispatcher(field_id):
        if field_id in financial_code.values():
            return 'financial'
        if field_id in project_code.values():
            return 'project'
        if field_id in intellectual_code.values():
            return 'intellectual'
        return None

    @staticmethod
    def my_financial_col_from_oracle_code(int_code):
        # return list(financial_code.keys())[list(financial_code.values()).index(int_code)]
        for k in financial_code.keys():
            if financial_code[k] == int_code:
                return k
        return None

    @staticmethod
    def my_intellectual_col_from_oracle_code(int_code):
        # return list(intellectual_code.keys())[list(intellectual_code.values()).index(int_code)]
        for k in intellectual_code.keys():
            if intellectual_code[k] == int_code:
                return k
        return None

    @staticmethod
    def my_project_col_from_oracle_code(int_code):
        # return list(project_code.keys())[list(project_code.values()).index(int_code)]
        for k in project_code.keys():
            if project_code[k] == int_code:
                return k
        return None
