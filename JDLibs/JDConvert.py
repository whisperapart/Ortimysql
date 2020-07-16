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
        xogg = defaultdict(lambda: 0)
        for key in ogg:
            xogg[key] = ogg[key] if ogg[key] is not None else 0
        ogg = xogg

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
        profile_str = ogg["COMPANY_PROFILE"]
        my["enterprise_info"] = '\'%s\'' % (profile_str[0:180])  # 企业介绍
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
    def ogg2mysql_user_login(ogg):
        xogg = defaultdict(lambda: 0)
        for key in ogg:
            xogg[key] = ogg[key] if ogg[key] is not None else 0
        ogg = xogg

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
        return my

    @staticmethod
    def ogg2mysql_financial(ogg):
        orc = JDCOracle()
        ret = orc.dynTableQuery(ogg['T_FIELD_NAME_ID'], ogg['T_TARGET_FORM_USER_ID'])
        orc.c()
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
        return my

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
        for k in financial_code.keys():
            if financial_code[k] == int_code:
                return k
        return None

    @staticmethod
    def my_intellectual_col_from_oracle_code(int_code):
        for k in intellectual_code.keys():
            if intellectual_code[k] == int_code:
                return k
        return None

    @staticmethod
    def my_project_col_from_oracle_code(int_code):
        for k in project_code.keys():
            if project_code[k] == int_code:
                return k
        return None
