|items| Source | Destination |
|:----|:----|----:|
|IP|192.168.1.88|192.168.1.157|
|User| oracle | root |
|DB|Oracle 11.2|MySQL5.7|
|OGG| OGG 12.1.2.1.0 for 11.2 | OGG bd	12.3.2.1.1 |
|Kafka| - | Kafka_2.11-2.4.0 |

## 1. source - oracle - install ogg 
- install path: /opt/ogg
- install db source: oracle 11.2

1. mkdir -p /opt/ogg
1. chown -R oracle:oinstall /opt/ogg
1. vi /etc/profile
```
export OGG_HOME=/opt/ogg
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/usr/lib
export PATH=$OGG_HOME:$PATH
```
1. source /etc/profile
1. su - oracle
1. sqlplus / as sysdba
1. archive log list
1. == if not ==
```
SQL> conn / as sysdba(以DBA身份连接数据库) 
SQL> shutdown immediate(立即关闭数据库)
SQL> startup mount(启动实例并加载数据库，但不打开)
SQL> alter database archivelog(更改数据库为归档模式)
SQL> alter database open(打开数据库)
SQL> alter system archive log start(启用自动归档)
alter database add supplemental log data(all) columns;
SQL> select supplemental_log_data_all from v$database; 
SUPPLEMEN
---------
YES
```

1. select force_logging, supplemental_log_data_min from v$database;
```
SQL> alter database force logging;
SQL> alter database add supplemental log data;
SQL> create tablespace oggtbs datafile '/usr/local/u01/oracle/oradata/oggtbs01.dbf' size 1000M autoextend on;
Tablespace created.
SQL>  create user ogg identified by ogg default tablespace oggtbs;
User created.
SQL> grant dba to ogg;
Grant succeeded.
select * from dba_sys_privs where GRANTEE='OGG';
```

1. su - oracle
1. cd /opt/ogg
1. ./ggsci
1. create subdirs
```
SQL> conn wuxihuishan_yutiaoshi/123456;
Connected.

GGSCI (VM_0_25_centos) 1> dblogin userid ogg password ogg
1. Successfully logged into database.
GGSCI (VM_0_25_centos) 3> view params ./globals
oggschema ogg

GGSCI (VM_0_25_centos) 4> edit param mgr
PORT 7809
DYNAMICPORTLIST 7810-7909
AUTORESTART EXTRACT *,RETRIES 5,WAITMINUTES 3
PURGEOLDEXTRACTS ./dirdat/*,usecheckpoints, minkeepdays 3

GGSCI (VM_0_25_centos) 7> add trandata wuxihuishan_yutiaoshi.user_info
Logging of supplemental redo data enabled for table WUXIHUISHAN_YUTIAOSHI.USER_INFO.
TRANDATA for scheduling columns has been added on table 'WUXIHUISHAN_YUTIAOSHI.USER_INFO'.
GGSCI (VM_0_25_centos) 8> info trandata wuxihuishan_yutiaoshi.user_info
Logging of supplemental redo log data is enabled for table TCLOUD.T_OGG.
Columns supplementally logged for table TCLOUD.T_OGG: ID.

GGSCI (VM_0_25_centos) 10> edit params ext2hd
extract ext2hd
dynamicresolution
GETUPDATEBEFORES
NOCOMPRESSDELETES
NOCOMPRESSUPDATES
SETENV (ORACLE_SID = "orcl")
SETENV (NLS_LANG = "american_america.AL32UTF8")
userid ogg,password ogg
exttrail /opt/ogg/dirdat/hs
table wuxihuishan_yutiaoshi.user_info;
table wuxihuishan_yutiaoshi.user_login;
table wuxihuishan_yutiaoshi.t_field_value_user;
table wuxihuishan_yutiaoshi.MANAG_USER;
table wuxihuishan_yutiaoshi.UPMS_ORGANIZATION;
table wuxihuishan_yutiaoshi.UPMS_USER_ORGANIZATION;

add extract ext2hd,tranlog,begin now
add exttrail /opt/ogg/dirdat/hs,extract ext2hd

start ext2hd
info all

edit params push2hd
extract push2hd
passthru
dynamicresolution
userid ogg,password ogg
rmthost 192.168.1.157 mgrport 7809
rmttrail /data/gg/dirdat/hs
table wuxihuishan_yutiaoshi.user_info;
table wuxihuishan_yutiaoshi.user_login;
table wuxihuishan_yutiaoshi.t_field_value_user;
table wuxihuishan_yutiaoshi.MANAG_USER;
table wuxihuishan_yutiaoshi.UPMS_ORGANIZATION;
table wuxihuishan_yutiaoshi.UPMS_USER_ORGANIZATION;

GGSCI (VM_0_25_centos) 17> add extract push2hd,exttrailsource /opt/ogg/dirdat/hs
EXTRACT added.
GGSCI (VM_0_25_centos) 18> add rmttrail /data/gg/dirdat/hs,extract push2hd
RMTTRAIL added.

edit params hs
defsfile /opt/ogg/dirdef/WUXIHUISHAN_YUTIAOSHI.USER_INFO
userid ogg,password ogg
table WUXIHUISHAN_YUTIAOSHI.USER_INFO;
table wuxihuishan_yutiaoshi.user_login;
table wuxihuishan_yutiaoshi.t_field_value_user;
table wuxihuishan_yutiaoshi.MANAG_USER;
table wuxihuishan_yutiaoshi.UPMS_ORGANIZATION;
table wuxihuishan_yutiaoshi.UPMS_USER_ORGANIZATION;
```
1. cd /opt/ogg
1. ./defgen paramfile dirprm/hs.prm
1. Definitions generated for 1 table in /opt/ogg/dirdef/WUXIHUISHAN_YUTIAOSHI.USER_INFO.
1. scp dirdef/WUXIHUISHAN_YUTIAOSHI.USER_INFO root@192.168.1.157:/data/gg/dirdef/


## 2. destination - ogg for bd

install openJDK set JAVA_HOME

vi /etc/profile
```
export OGG_HOME=/data/gg
export LD_LIBRARY_PATH=$JAVA_HOME/jre/lib/amd64:$JAVA_HOME/jre/lib/amd64/server:$JAVA_HOME/jre/lib/amd64/libjsig.so:$JAVA_HOME/jre/lib/amd64/server/libjvm.so:$OGG_HOME/lib
export PATH=$OGG_HOME:$PATH
```
ggsci
```
create subdirs
edit params mgr
PORT 7809
DYNAMICPORTLIST 7810-7909
AUTORESTART EXTRACT *,RETRIES 5,WAITMINUTES 3
PURGEOLDEXTRACTS ./dirdat/*,usecheckpoints, minkeepdays 3

edit  params  ./GLOBALS
CHECKPOINTTABLE WUXIHUISHAN_YUTIAOSHI.checkpoint

edit params rekafka
REPLICAT rekafka
sourcedefs /data/gg/dirdef/WUXIHUISHAN_YUTIAOSHI.USER_INFO
TARGETDB LIBFILE libggjava.so SET property=dirprm/kafka.props
REPORTCOUNT EVERY 1 MINUTES, RATE 
GROUPTRANSOPS 10000
MAP WUXIHUISHAN_YUTIAOSHI.*, TARGET WUXIHUISHAN_YUTIAOSHI.*;


```
vi rekafka.prm
```
gg.handlerlist=kafkahandler
gg.handler.kafkahandler.type=kafka
gg.handler.kafkahandler.KafkaProducerConfigFile=custom_kafka_producer.properties
gg.handler.kafkahandler.topicMappingTemplate=togg
gg.handler.kafkahandler.format=json
gg.handler.kafkahandler.mode=tx
gg.handler.kafkahandler.format.includePrimaryKeys=true
gg.classpath=dirprm/:/opt/module/kafka_2.11-2.4.0/libs/*:/data/gg/:/data/gg/lib/*
```
vi custom_kafka_producer.properties
```
bootstrap.servers=192.168.1.157:9092
acks=1
compression.type=gzip
reconnect.backoff.ms=1000
value.serializer=org.apache.kafka.common.serialization.ByteArraySerializer
key.serializer=org.apache.kafka.common.serialization.ByteArraySerializer
batch.size=102400
linger.ms=10000
```
add replicat rekafka exttrail /data/gg/dirdat/hs,checkpointtable WUXIHUISHAN_YUTIAOSHI.checkpoint


source : ls -l /opt/ogg/dirdat/hs*
dest: ls -l /data/gg/dirdat/hs*

## 3. destination install kafka

- https://blog.csdn.net/csdnlihai/article/details/87787236

1. wget https://mirrors.cnnic.cn/apache/kafka/2.4.0/kafka_2.11-2.4.0.tgz --no-check-certificate
1. tar zxvf kafka_2.11-2.4.0.tgz

bin/kafka-console-consumer.sh --bootstrap-server 192.168.1.157:9092 --topic togg --from-beginning
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
 
cd /lib/systemd/system/ 
vim zookeeper.service 

```
[Unit]
Description=Zookeeper service
After=network.target

[Service]
Type=simple
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.181-7.b13.el7.x86_64/jre/bin"
User=root
Group=root
ExecStart=/opt/module/kafka_2.11-2.4.0/bin/zookeeper-server-start.sh /opt/module/kafka_2.11-2.4.0/config/zookeeper.properties
ExecStop=/opt/module/kafka_2.11-2.4.0/bin/zookeeper-server-stop.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```


vim kafka.service 

```
Description=Apache Kafka server (broker)
After=network.target  zookeeper.service

[Service]
Type=simple
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.181-7.b13.el7.x86_64/jre/bin"
User=root
Group=root
ExecStart=/opt/module/kafka_2.11-2.4.0/bin/kafka-server-start.sh /opt/module/kafka_2.11-2.4.0/config/server.properties
ExecStop=/opt/module/kafka_2.11-2.4.0/bin/kafka-server-stop.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### 安装为service
 ```
 # systemctl daemon-reload
 ```

zookeeper、kafka服务加入开机自启。 
 ```
 # systemctl enable zookeeper
 # systemctl enable kafka
 ```
4. 使用systemctl启动/关闭/重启 zookeeper、kafka服务systemctl start/stop/restart  zookeeper/kafka。

注：启动kafka前必须先启动zookeeper 。
 ```
 # systemctl start zookeeper
 # systemctl start kafka
 ```



./bin/kafka-topics.sh --delete --bootstrap-server 192.168.1.157:9092 --topic togg
/opt/module/kafka_2.11-2.4.0/bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list 192.168.1.157:9092 --topic togg
