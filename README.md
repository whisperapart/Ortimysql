# Oracle Real TIme to MYSQL
## description 
 - A daemon program for realtime-synchronizing from oracle to mysql
 - Python/ Kafka / oracle / mysql / realtime data sync
 - Supports dynamic/custom table/columns with different data types
 - Write convert rules in JDConvert.py
<p>中文表述</p>

 - Oracle 数据实时同步至 Mysql
 - 实现不同表不同字段不同类型的映射
 - 启动为守护进程
 - 需要自定义转换规则

## usage
 - prerequisite : [oracle_to_kafka](./Docs/oggKafka.md)
 - run o2m.py to consume message from kafka
```bash
 # python o2m.py
Usage: python filename.py [option]
	 start 		start daemon
	 stop 		stop daemon
	 restart 	restart
	 status 	check status
	 forceInit 	redo queue
```

 - **optional** run syncInit.py to send all oracle table-data into kafka
```bash
 # python syncInit.py 
Usage: python syncInit.py [option] <table_name>
	 forceDrop 		Force to DROP MySQL Table
	 insertAll 		Insert all rows from oracle to kafka
```

 - **optional** run util_compile.py to get a executable release
```bash
 # python util_compile.py
```

## environments
|items| Source | Destination |
|:----|:----|:----|
|IP|192.168.1.88|192.168.1.157|
|User| oracle | root |
|DB|Oracle 11.2|MySQL5.7|
|OGG| OGG 12.1.2.1.0 for 11.2 | OGG bd	12.3.2.1.1 |
|Kafka| - | Kafka_2.11-2.4.0 |

### python 3.7.7:
```bash
 # wget -c https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz
 # tar -zxvf python-3.7.7.tgz
 # cd python-3.7.7
 # mkdir -p /usr/local/python3
 # ./configure --prefix=/usr/local/python3
 # make && make install
 # ln -s /usr/local/python3/bin/python3 /usr/local/bin/python3
 # ln -s /usr/local/python3/bin/pip3 /usr/local/bin/pip3
 # python3 -V
 # pip3 --version
```

## tables
|Map Type| Oracle(Source) | MySql(Destination) |
|:----|:----|:----|
|normal| USER_INFO | user_info |
|normal| USER_LOGIN | user_login |
|normal| MANAG_USER | manag_user |
|normal| UPMS_ORGANIZATION | upms_organization |
|normal| UPMS_USER_ORGANIZATION | upms_user_organization |
|dynamic| T_FIELD_VALUE_USER | t_project_info |
|dynamic| T_FIELD_VALUE_USER | t_user_intellectual |
|dynamic| T_FIELD_VALUE_USER | t_user_financial |
