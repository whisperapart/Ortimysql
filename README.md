# PolicyAnalyze
<p>
A sample daemon program for realtime-synchronizing from oracle to mysql.<br>
Python/ Kafka / oracle / mysql / realtime data sync<br>
Supports dynamic/custom table/columns with different data types.
</p>
<p>
Oracle 数据实时同步至 Mysql，实现不同表不同字段不同类型的映射。<br>
启动为守护进程。
</p>

## usage
1. run o2m.py to consume message from kafka
```shell script
$ python o2m.py
Usage: python filename.py [option]
	 start 		start daemon
	 stop 		stop daemon
	 restart 	restart
	 status 	check status
	 forceInit 	redo queue
```

2. [optional] run syncInit.py to send all oracle table-data into kafka
```shell script
$ python syncInit.py 
Usage: python syncInit.py [option] <table_name>
	 forceDrop 		Force to DROP MySQL Table
	 insertAll 		Insert all rows from oracle to kafka
```

3. [optional] run util_compile.py to get a executable release
```shell script
$ python util_compile.py
```

## environments
|items| Source | Destination |
|:----|:----|:----|
|IP|192.168.1.88|192.168.1.157|
|User| oracle | root |
|DB|Oracle 11.2|MySQL5.7|
|OGG| OGG 12.1.2.1.0 for 11.2 | OGG bd	12.3.2.1.1 |
|Kafka| - | Kafka_2.11-2.4.0 |

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
