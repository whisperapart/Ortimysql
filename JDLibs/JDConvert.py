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

sys_company_type = {
    '100': '国有及控股企业', '101': '集团企业', '102': '股份合作企业', '103': '联营企业',
    '104': '有限责任公司', '105': '股份有限公司', '106': '私营企业', '107': '港澳台商投资企业',
    '108': '港澳台投资股份有限公司', '109': '外商投资公司', '110': '合资企业', '111': '其他企业'
}

sys_reg_status = {
    '1': '存续（在营、开业、在册）', '2': '吊销，未注销', '3': '吊销，已注销', '4': '注销', '5': '迁出'
}

sys_board = {
    '1': '主板', '2': '新三板', '3': '创业板', '4': '科创板', '5': '其他'
}

sys_tech = {
    '10101':'基础软件','10102':'嵌入式软件','10103':'计算机辅助设计与辅助工程管理软件','10104':'中文及多语种处理软件','10105':'图形和图像处理软件','10106':'地理信息系统（GIS）软件','10107':'电子商务软件','10108':'电子政务软件','70':'资源与环境','10109':'企业管理软件','10110':'物联网应用软件','10111':'云计算与移动互联网软件','10112':'Web服务与集成软件','10201':'集成电路设计技术','10202':'集成电路产品设计技术','10203':'集成电路封装技术','10204':'集成电路测试技术','10205':'集成电路芯片制造工艺技术','10206':'集成光电子器件设计、制造与工艺技术','80':'先进制造与自动化','10301':'计算机及终端设计与制造技术','10302':'计算机外围设备设计与制造技术','10303':'网络设备设计与制造技术','10304':'网络应用技术','10401':'通信网络技术','10402':'光传输系统技术','10403':'有线宽带接入系统技术','10404':'移动通信系统技术','10405':'宽带无线通信系统技术','10406':'卫星通信系统技术','10407':'微波通信系统技术','10408':'物联网设备、部件及组网技术','10409':'电信网络运营支撑管理技术','10410':'电信网与互联网增值业务应用技术','10501':'广播电视节目采编播系统技术','10502':'广播电视业务集成与支撑系统技术','10503':'有线传输与覆盖系统技术','10504':'无线传输与覆盖系统技术','10505':'广播电视监测监管、安全运行与维护系统技术','10506':'数字电影系统技术','107':'信息安全技术','30105':'空中管制技术','30106':'民航及通用航空运行保障技术','30201':'卫星总体技术','30202':'运载火箭技术','30203':'卫星平台技术','70205':'有限空间空气污染防治技术','70301':'危险固体废弃物处置技术','70302':'工业固体废弃物综合利用技术','70303':'生活垃圾处置与资源化技术','30204':'卫星有效载荷技术','108':'智能交通和轨道交通技术','30205':'航天测控技术','30206':'航天电子与航天材料制造技术','30207':'先进航天动力设计技术','30208':'卫星应用技术','40101':'精品钢材制备技术','40102':'铝、铜、镁、钛合金清洁生产与深加工技术','40103':'稀有、稀土金属精深产品制备技术','40104':'纳米及粉末冶金新材料制备与应用技术','40105':'金属及金属基复合新材料制备技术','40106':'半导体新材料制备与应用技术','201':'医药生物技术','40107':'电工、微电子和光电子新材料制备与应用技术','40108':'超导、高效能电池等其它新材料制备与应用技术','40201':'结构陶瓷及陶瓷基复合材料强化增韧技术','40202':'功能陶瓷制备技术','40203':'功能玻璃制备技术','40204':'节能与新能源用材料制备技术','40205':'环保及环境友好型材料技术','40301':'新型功能高分子材料的制备及应用技术','40302':'工程和特种工程塑料制备技术','40303':'新型橡胶的合成技术及橡胶新材料制备技术','202':'中药、天然药物','40304':'新型纤维及复合材料制备技术','40305':'高分子材料制备及循环再利用技术','40306':'高分子材料的新型加工和应用技术','40401':'介入治疗器具材料制备技术','40402':'心脑血管外科用新型生物材料制备技术','40403':'骨科内置物制备技术 ','40404':'口腔材料制备技术','40405':'组织工程用材料制备技术','40406':'新型敷料和止血材料制备技术','40407':'专用手术器械和材料制备技术','20':'生物与新医药','203':'化学药研发技术','40408':'其他新型医用材料及制备技术','40501':'新型催化剂制备及应用技术','40502':'电子化学品制备及应用技术','40503':'超细功能材料制备及应用技术','40504':'精细化学品制备及应用技术','40601':'文化载体和介质新材料制备技术','40602':'艺术专用新材料制备技术','40603':'影视场景和舞台专用新材料的加工生产技术','40604':'文化产品印刷新材料制备技术','40605':'文物保护新材料制备技术','204':'药物新剂型与制剂创制技术','50101':'研发服务','50102':'设计服务','50201':'检验检测认证技术','50202':'标准化服务技术','50301':'云计算服务技术','50302':'数据服务技术','50303':'其他信息服务技术','50601':'电子商务技术','50602':'物流与供应链管理技术','50701':'智慧城市服务支撑技术','205':'医疗仪器、设备与医学专用软件','50702':'互联网教育','50703':'健康管理','50704':'现代体育服务支撑技术','50801':'创作、设计与制作技术','50802':'传播与展示技术','50803':'文化遗产发现与再利用技术','50804':'运营与管理技术','60101':'太阳能','60102':'风能','60103':'生物质能','206':'轻工和化工生物技术','60104':'地热能、海洋能及运动能','60201':'核能','60202':'氢能','60301':'高性能绿色电池（组）技术','60302':'新型动力电池（组）与储能电池技术','60303':'燃料电池技术','60304':'超级电容器与热电转换技术','60401':'工业节能技术','60402':'能量回收利用技术','60403':'蓄热式燃烧技术','207':'农业生物技术','60404':'输配电系统优化技术','60405':'高温热泵技术','60406':'建筑节能技术','60407':'能源系统管理、优化与控制技术','60408':'节能监测技术','70101':'城镇污水处理与资源化技术','70102':'工业废水处理与资源化技术','70103':'农业水污染控制技术','30101':'飞行器','30102':'飞行器动力技术','30103':'飞行器系统技术','30104':'飞行器制造与材料技术','70201':'煤燃烧污染防治技术','70202':'机动车排放控制技术','70203':'工业炉窑污染防治技术','70204':'工业有害废气控制技术','302':'航天技术','70304':'建筑垃圾处置与资源化技术','70305':'有机固体废物处理与资源化技术','70306':'社会源固体废物处置与资源化技术','70401':'噪声、振动污染防治技术','70402':'核与辐射安全防治技术','70501':'环境监测预警技术','70502':'应急环境监测技术','70503':'生态环境监测技术','70504':'非常规污染物监测技术','70701':'重污染行业生产过程中节水、减排及资源化关键技术','401':'金属材料','70702':'清洁生产关键技术','70703':'环保制造关键技术','70801':'资源勘查开采技术','70802':'提高矿产资源回收利用率的采矿、选矿技术','70803':'伴生有价元素的分选提取技术','70804':'低品位资源和尾矿资源综合利用技术','70805':'放射性资源勘查开发技术','70806':'放射性废物处理处置技术','70807':'绿色矿山建设技术','80101':'现场总线与工业以太网技术','402':'无机非金属材料','80102':'嵌入式系统技术','80103':'新一代工业控制计算机技术','80104':'制造执行系统（MES）技术','80105':'工业生产过程综合自动化控制系统技术','80201':'矿山安全生产技术','80202':'危险化学品安全生产技术','80203':'其它事故防治及处置技术','80301':'新型传感器','80302':'新型自动化仪器仪表','80303':'科学分析仪器/检测仪器','403':'高分子材料','80304':'精确制造中的测控仪器仪表','80305':'微机电系统技术','80401':'高档数控装备与数控加工技术','80402':'机器人','80403':'智能装备驱动控制技术','80404':'特种加工技术','80405':'大规模集成电路制造相关技术','80406':'增材制造技术','80407':'高端装备再制造技术','80501':'机械基础件及制造技术','30':'航空航天','404':'生物医用材料','80502':'通用机械装备制造技术','80503':'极端制造与专用机械装备制造技术','80504':'纺织及其他行业专用设备制造技术','80601':'发电与储能技术','80602':'输电技术','80603':'配电与用电技术','80604':'变电技术','80605':'系统仿真与自动化技术','80701':'车用发动机及其相关技术','80702':'汽车关键零部件技术','405':'精细和专用化学品','80703':'节能与新能源汽车技术','80704':'机动车及发动机先进设计、制造和测试平台技术','80705':'轨道车辆及关键零部件技术','80801':'高技术船舶设计制造技术','80802':'海洋工程装备设计制造技术','80901':'乐器制造技术','80902':'印刷技术','406':'与文化艺术产业相关的新材料','501':'研发与设计服务','502':'检验检测认证与标准服务','503':'信息技术服务','504':'高技术专业化服务','505':'知识产权与成果转化服务','506':'电子商务与现代物流技术','507':'城市管理与社会服务','40':'新材料','508':'文化创意产业支撑技术','601':'可再生清洁能源','602':'核能及氢能','603':'新型高效能量转换与储存技术','604':'高效节能技术','701':'水污染控制与水资源利用技术','702':'大气污染控制技术','703':'固体废弃物处置与综合利用技术','704':'物理性污染防治技术','705':'环境监测及环境事故应急处理技术','50':'高技术服务','706':'生态环境建设与保护技术','707':'清洁生产技术','708':'资源勘查、高效开采与综合利用技术','801':'工业生产过程控制系统','802':'安全生产技术 ','803':'高性能、智能化仪器仪表','804':'先进制造工艺与装备','805':'新型机械','806':'电力系统与设备','807':'汽车及轨道车辆相关技术','60':'新能源与节能','808':'高技术船舶与海洋工程装备设计制造技术','809':'传统文化产业改造技术','10':'电子信息','101':'软件','10507':'数字电视终端技术','10508':'专业视频应用服务平台技术','10509':'音响、光盘技术','10601':'半导体发光技术','10602':'片式和集成无源元件','10603':'大功率半导体器件','10604':'专用特种器件','10605':'敏感元器件与传感器','10606':'中高档机电组件','10607':'平板显示器件','102':'微电子技术','10701':'密码技术','10702':'认证授权技术','10703':'系统与软件安全技术','10704':'网络与通信安全技术','10705':'安全保密技术','10706':'安全测评技术','10707':'安全管理技术','10708':'应用安全技术','10801':'交通控制与管理技术','10802':'交通基础信息采集、处理技术','103':'计算机产品及其网络应用技术','10803':'交通运输运营管理技术','10804':'车、船载电子设备技术','10805':'轨道交通车辆及运行保障技术','10806':'轨道交通运营管理与服务技术','20101':'新型疫苗','20102':'生物治疗技术和基因工程药物','20103':'快速生物检测技术','20104':'生物大分子类药物研发技术','20105':'天然药物生物合成制备技术','20106':'生物分离介质、试剂、装置及相关检测技术','104':'通信技术','20201':'中药资源可持续利用与生态保护技术','20202':'创新药物研发技术','20203':'中成药二次开发技术','20204':'中药质控及有害物质检测技术','20301':'创新药物技术','20302':'手性药物创制技术','20303':'晶型药物创制技术','20304':'国家基本药物生产技术','20305':'国家基本药物原料药和重要中间体的技术','20401':'创新制剂技术','105':'广播影视技术','20402':'新型给药制剂技术','20403':'制剂新辅料开发及生产技术','20404':'制药装备技术','20501':'医学影像诊断技术','20502':'新型治疗、急救与康复技术','20503':'新型电生理检测和监护技术','20504':'医学检验技术及新设备','20505':'医学专用网络新型软件','20506':'医用探测及射线计量检测技术','20601':'高效工业酶制备与生物催化技术','106':'新型电子元器件','20602':'微生物发酵技术','20603':'生物反应及分离技术','20604':'天然产物有效成份的分离提取技术','20605':'食品安全生产与评价技术','20606':'食品安全检测技术','20701':'农林植物优良新品种与优质高效安全生产技术','20702':'畜禽水产优良新品种与健康养殖技术','20703':'重大农林生物灾害与动物疫病防控技术','20704':'现代农业装备与信息化技术','20705':'农业面源和重金属污染农田综合防治与修复技术','70104':'流域水污染治理与富营养化综合控制技术','70105':'节水与非常规水资源综合利用技术','301':'航空技术','70106':'饮用水安全保障技术'
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
    'total_new_drug_certificate': 12410,  # 新药证书总量
    # 'year': # 年份 todo: 编号待补全
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
    'year': 11791  # 年份
}

project_map = {
    "'国家高新技术企业认定'": {"name": '\'%s\'' % "国家高新技术企业认定", "level": '\'%s\'' % "国家级", "window": '\'%s\'' % "科技",
                     "project_type": 5},
    "'国家科技型中小企业'": {"name": '\'%s\'' % "江苏省科技型中小企业", "level": '\'%s\'' % "省级", "window": '\'%s\'' % "科技",
                    "project_type": 5},
    "'江苏省高新技术企业（培育入库）企业'": {"name": '\'%s\'' % "国家科技型中小企业信息库入库企业", "level": '\'%s\'' % "省级", "window": '\'%s\'' % "科技",
                            "project_type": 5},
    "'江苏省创新型领军企业'": {"name": '\'%s\'' % "江苏省创新型领军企业", "level": '\'%s\'' % "省级", "window": '\'%s\'' % "科技",
                     "project_type": 5},
    "'江苏省企业技术创新奖'": {"name": '\'%s\'' % "江苏省企业技术创新奖", "level": '\'%s\'' % "省级", "window": '\'%s\'' % "科技",
                     "project_type": 5},
    "'江苏省农业产业化重点龙头企业'": {"name": '\'%s\'' % "省重点研发计划（现代农业）项目", "level": '\'%s\'' % "省级", "window": '\'%s\'' % "科技",
                         "project_type": 5},
    "'知识产权贯标企业'": {"name": '\'%s\'' % "江苏省企业知识产权管理标准化贯标奖励", "level": '\'%s\'' % "省级", "window": '\'%s\'' % "知产",
                   "project_type": 7}
}


# 载体项目=1，知识产权项目=2，人才项目=3，经信项目=4，科技项目=5，发改项目=6，体系资质=7


def fix_project_info(p):
    for m in project_map:
        if m == p["project_name"]:
            # if p["project_name"] in project_map:
            # print("key matches: %s" % p["project_name"])
            p["project_name"] = project_map[m]["name"]
            p["level"] = project_map[m]["level"]
            p["window"] = project_map[m]["window"]
            p["project_type"] = project_map[m]["project_type"]
    return p


class JDConvert:
    @staticmethod
    def areaCodeToName(code):
        c = str(code)
        return sys_area[c] if c in sys_area else sys_area['450102009']

    @staticmethod
    def companyTypeToString(code):
        c = str(code)
        return sys_company_type[c] if c in sys_company_type else sys_company_type['111']

    @staticmethod
    def companyRegStatusToString(code):
        c = str(code)
        return sys_reg_status[c] if c in sys_reg_status else sys_reg_status['5']

    @staticmethod
    def boardToString(code):
        c = str(code)
        return sys_board[c] if c in sys_board else sys_board['5']

    @staticmethod
    def techToString(code):
        c = str(code)
        return sys_tech[c] if c in sys_tech else sys_tech['10']

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
        my["enterprise_nature"] = '\'%s\'' % JDConvert.companyTypeToString(ogg["COMPANY_TYPE_A"])  # 企业性质
        my["paper_type"] = 0 if ogg["PAPER_TYPE_ABCDEF"] is None else ogg["PAPER_TYPE_ABCDEF"]  # 证件类型
        my["area_id_c"] = '\'%s\'' % JDConvert.areaCodeToName(ogg["AREA_ID_C_ABCDEF"])  # 所属地区县
        my["area_id_b"] = '\'%s\'' % JDConvert.areaCodeToName(ogg["AREA_ID_B_ABCDEF"])  # 所属地区市
        my["area_id_a"] = '\'%s\'' % JDConvert.areaCodeToName(ogg["AREA_ID_A_ABCDEF"])  # 所属地区省
        my["area_id"] = '\'%s\'' % JDConvert.areaCodeToName(ogg["AREA_ID_ABCDEF"])  # 所属地区
        my["is_legal_person"] = '\'是\'' if str(ogg["INDEPENTDENT_LEGAL_PERSON"]) == '1' else '\'否\''  # 是否独立法人
        my["legal_person"] = '\'%s\'' % ogg["HQ_LEGAL_PERSON_C"]  # 法人
        # my["legal_person_degree"] = ogg[""]     # 法人学历
        my["legal_person_phone"] = '\'%s\'' % ogg["LEGAL_PERSON_TEL"]  # 法人手机
        # my["regist_capital"] = 0 if ogg["REGIST_CAPITAL_AC"] is None else ogg["REGIST_CAPITAL_AC"]  # 注册资本
        my["regist_capital"] = ogg["REGIST_CAPITAL_AC"]  # 注册资本
        my["regist_time"] = '\'%s\'' % ogg["REGIST_TIME_ABCE"] if ogg["REGIST_TIME_ABCE"] != 0 else 0  # 注册时间
        my["register_status"] = '\'%s\'' % JDConvert.companyRegStatusToString(ogg["REGISTER_STATUS"])  # 登记状态
        my["addr"] = '\'%s\'' % ogg["ADDR_ABCDEF"]  # 通讯地址
        my["technology_field"] = '\'%s\'' % JDConvert.techToString(ogg["TECHNOLOGY_FIELD"])  # 技术领域
        my["national_economy_industry"] = '\'\'' if ogg["NATIONAL_ECONOMY_INDUSTRY"]==0 else '\'%s\'' % ogg["NATIONAL_ECONOMY_INDUSTRY"]  # 国民经济行业
        my["enterprise_attribute"] = '\'%s\'' % ogg["COMPANY_ATTRIBUTE"]  # 企业属性
        my["enterprise_scale"] = '\'%s\'' % ogg["COMPANY_SCALE"]  # 企业规模
        my["is_gauge"] = '\'是\'' if str(ogg["IS_GAUGE"]) == '1' else '\'否\''  # 规上企业0否1是
        my["credit_rating"] = '\'%s\'' % ogg["COMPANY_CREDIT_RATING"]  # 资信等级
        my["is_listed"] = '\'是\'' if str(ogg["IS_ON_LISTED"]) == '1' else '\'否\''  # 是否上市
        my["listing_sector"] = '\'%s\'' % JDConvert.boardToString(ogg["COMPANY_LISTING_SECTOR"])  # 其中上市板块
        my["master_project"] = '\'%s\'' % ogg["MAIN_PRODUCT_A"]  # 主营业务及产品
        # my["market_guonei"] = ogg[""]           # 产品国内市场份额
        # my["market_guowai"] = ogg[""]           # 产品国外市场份额
        # my["sources"] = ogg[""]                 # 信息来源
        # my["core_technology_sources"] = ogg[""] # 核心技术来源
        profile_str = str(ogg["COMPANY_PROFILE"])
        my["enterprise_info"] = '\'%s\'' % (profile_str[0:180])  # 企业介绍
        my["open_bank"] = '\'\'' if ogg["BANK_OPEN_ABCDEF"] == 0 else '\'%s\'' % ogg["BANK_OPEN_ABCDEF"]  # 开户行
        my["open_bank_no"] = '\'\'' if ogg["BANK_ACCOUNT_ABCDEF"] == 0 else '\'%s\'' % ogg["BANK_ACCOUNT_ABCDEF"]  # 开户账号
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
    def ogg2mysql_user_contact(ogg):
        xogg = defaultdict(lambda: 0)
        for key in ogg:
            xogg[key] = ogg[key] if ogg[key] is not None else 0
        ogg = xogg

        contact = {
            "id": "%s%s" % (ogg["USER_ID"], "01"),
            "name": '\'%s\'' % ogg["CONTACTS_ABCDEF"],
            "mobile": '\'%s\'' % ogg["MOVE_TEL_ABCDEF"],
            "duty": '\'%s\'' % "联系人",  # 职务 varchar50
            "email": '\'%s\'' % ogg["EMAIL_ABCDEF"],  # 职务 varchar50
            "is_delete": 2,
            "user_id": ogg["USER_ID"],  # 用户id bigint20
            "user_name": '\'%s\'' % ogg["USER_NAME_ABCDEF"],  # 用户名称 - 企业名称 varchr 100
            "paper_no": '\'%s\'' % ogg["PAPER_NO_ABCDEF"]  # 证件号码 varchar 100
        }
        financial = {
            "id": "%s%s" % (ogg["USER_ID"], "02"),
            "name": '\'%s\'' % ogg["FINANCE_CONTACT"],
            "mobile": '\'%s\'' % ogg["FINANCE_MOBEL"],
            "duty": '\'%s\'' % "财务",  # 职务 varchar50
            "email": '\'%s\'' % ogg["FINANCE_EMAIL"],  # 职务 varchar50
            "is_delete": 2,
            "user_id": ogg["USER_ID"],  # 用户id bigint20
            "user_name": '\'%s\'' % ogg["USER_NAME_ABCDEF"],  # 用户名称 - 企业名称 varchr 100
            "paper_no": '\'%s\'' % ogg["PAPER_NO_ABCDEF"]  # 证件号码 varchar 100
        }
        my = []
        if contact['name'] != '':
            my.append(contact)
        if financial['name'] != '':
            my.append(financial)
        # my['id'] = '\'%s\'' % ogg[""]  # id primary key 非空 bigint 20
        # my['type'] = '\'%s\'' % ogg[""]  # 联系人类型 varchar 10
        # my['name'] = '\'%s\'' % ogg["CONTACTS_ABCDEF"]  # 联系人 varchar 32
        # my['qq'] = '\'%s\'' % ogg[""]  # qq varchar20
        # my['email'] = '\'%s\'' % ogg[""]  # 邮箱 varchar50
        # my['mobile'] = '\'%s\'' % ogg["MOVE_TEL_ABCDEF"]  # 手机 varchar20
        # my['duty'] = '\'%s\'' % ogg[""]  # 职务 varchar50
        # my['department'] = '\'%s\'' % ogg[""]  # 所属部门 varchar50
        # my['is_delete'] = '\'%s\'' % ogg[""]  # 1删除 2未删除 int1
        # my['source'] = '\'%s\'' % ogg[""]  # 来源1导入2创建 int1
        # my['user_id'] = '\'%s\'' % ogg[""]  # 用户id bigint20
        # my['create_time'] = '\'%s\'' % ogg[""]  # 创建时间 datetime
        # my['update_time'] = '\'%s\'' % ogg[""]  # 更新时间 非空 timestamp
        # my['user_name'] = '\'%s\'' % ogg[""]  # 用户名称 - 企业名称 varchr 100
        # my['paper_no'] = '\'%s\'' % ogg[""]  # 证件号码 varchar 100
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
        my['ID'] = int(ogg['ID'])  # ID bigint 20
        my['SYS_ID'] = '\'%s\'' % ogg['SYS_ID']  # 系统地区ID varchar 50
        my['MANAG_ID'] = '\'%s\'' % ogg['MANAG_ID']  # varchar 100
        my['MANAG_PW'] = '\'%s\'' % ogg['MANAG_PW']  # varchar 255
        my['STATE'] = int(ogg['STATE'])  # smallint 2
        my['IS_DELETE'] = int(ogg['IS_DELETE'])  # smallint 2
        my['BEF_SYS_ID'] = '\'%s\'' % ogg['BEF_SYS_ID']  # varchar 50
        my['BEF_LOGINTIME'] = '\'%s\'' % ogg["BEF_LOGINTIME"] if ogg["BEF_LOGINTIME"] != 0 else 0  # datetime
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
        my['create_time'] = '\'%s\'' % ogg["CTIME"] if ogg["CTIME"] != 0 else 0  # timestamp
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
        print("inside call")
        try:
            orc = JDCOracle()
            ret = orc.dynTableQuery(ogg['T_FIELD_NAME_ID'], ogg['T_TARGET_FORM_USER_ID'])
            orc.c()
        except Exception as e:
            print(e)
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
                    y = x if x > 0 else 0
                    my['year'] = '\'%s\'' % y
            # 项目表中的 year 字段
            if k == 'year' and d['VALUE'] is not None:
                try:
                    my['year'] = int(d['VALUE'])
                except:
                    continue
        my = fix_project_info(my)
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
                    dv = d['VALUE']
                    try:
                        dv = int(d['VALUE'])
                    except ValueError:
                        try:
                            dv = float(d['VALUE'])
                            dv = round(dv, 2)
                        except ValueError:
                            dv = d['VALUE']  # string

                    my[k] = dv
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
                try:
                    my['year'] = int(d['VALUE'])
                except:
                    continue
            # 解决mysql 逻辑删除问题
            my['is_delete'] = 2
        return my

    @staticmethod
    def ogg2mysql_intellectual(ogg):
        orc = JDCOracle()
        ret = orc.dynTableQuery(ogg['T_FIELD_NAME_ID'], ogg['T_TARGET_FORM_USER_ID'])
        orc.c()
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
                    y = x if x > 0 else 0
                    my['year'] = '\'%s\'' % y
            if k == 'year' and d['VALUE'] is not None:
                try:
                    my['year'] = int(d['VALUE'])
                except:
                    continue
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
