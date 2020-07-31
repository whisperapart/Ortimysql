# Ogg to Kafka
## 0. environments
|items| Source | Destination |
|:----|:----|----:|
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

## 1. source - oracle - install ogg 
- pre-installed oracle version: oracle 11.2
- ogg installation path: /opt/ogg

```bash
 # mkdir -p /opt/ogg
 # chown -R oracle:oinstall /opt/ogg
 # vi /etc/profile
export OGG_HOME=/opt/ogg
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/usr/lib
export PATH=$OGG_HOME:$PATH
 # source /etc/profile
 # su - oracle
 # sqlplus / as sysdba
 # archive log list
```

如果archive模式未启动，执行以下命令:
```bash
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

创建同步所需要的库、用户：
```bash
SQL> select force_logging, supplemental_log_data_min from v$database;
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

启动ogg，并创建目录：
```bash
 # su - oracle
 # cd /opt/ogg
 # ./ggsci
SQL> create subdirs
SQL> conn wuxihuishan_yutiaoshi/123456;
Connected.
```

创建同步用户，并编辑mgr参数
```bash
1> dblogin userid ogg password ogg
1. Successfully logged into database.
3> view params ./globals
oggschema ogg

4> edit param mgr
PORT 7809
DYNAMICPORTLIST 7810-7909
AUTORESTART EXTRACT *,RETRIES 5,WAITMINUTES 3
PURGEOLDEXTRACTS ./dirdat/*,usecheckpoints, minkeepdays 3
```

配置同步表信息
```bash
7> add trandata wuxihuishan_yutiaoshi.user_info
Logging of supplemental redo data enabled for table WUXIHUISHAN_YUTIAOSHI.USER_INFO.
TRANDATA for scheduling columns has been added on table 'WUXIHUISHAN_YUTIAOSHI.USER_INFO'.
8> info trandata wuxihuishan_yutiaoshi.user_info
Logging of supplemental redo log data is enabled for table wuxihuishan_yutiaoshi.user_info.
Columns supplementally logged for table wuxihuishan_yutiaoshi.user_info: ID.
```

配置抽取
```bash
10> edit params ext2hd
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

11> add extract ext2hd,tranlog,begin now
12> add exttrail /opt/ogg/dirdat/hs,extract ext2hd

13> start ext2hd
14> info all
```

配置推送
```bash
15> edit params push2hd
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

17> add extract push2hd,exttrailsource /opt/ogg/dirdat/hs
EXTRACT added.
18> add rmttrail /data/gg/dirdat/hs,extract push2hd
RMTTRAIL added.
```

配置映射：
```bash
19> edit params hs
defsfile /opt/ogg/dirdef/WUXIHUISHAN_YUTIAOSHI.USER_INFO
userid ogg,password ogg
table WUXIHUISHAN_YUTIAOSHI.USER_INFO;
table wuxihuishan_yutiaoshi.user_login;
table wuxihuishan_yutiaoshi.t_field_value_user;
table wuxihuishan_yutiaoshi.MANAG_USER;
table wuxihuishan_yutiaoshi.UPMS_ORGANIZATION;
table wuxihuishan_yutiaoshi.UPMS_USER_ORGANIZATION;
```

创建映射文件：
```bash
 # cd /opt/ogg
 # ./defgen paramfile dirprm/hs.prm
Definitions generated for 1 table in /opt/ogg/dirdef/WUXIHUISHAN_YUTIAOSHI.USER_INFO.
```

复制到目标服务器：
```bash
 # scp dirdef/WUXIHUISHAN_YUTIAOSHI.USER_INFO root@192.168.1.157:/data/gg/dirdef/
```


## 2. destination - ogg for bd
install openJDK set JAVA_HOME
```bash
 # vi /etc/profile
export OGG_HOME=/data/gg
export LD_LIBRARY_PATH=$JAVA_HOME/jre/lib/amd64:$JAVA_HOME/jre/lib/amd64/server:$JAVA_HOME/jre/lib/amd64/libjsig.so:$JAVA_HOME/jre/lib/amd64/server/libjvm.so:$OGG_HOME/lib
export PATH=$OGG_HOME:$PATH
```

创建目录：
```bash
 # cd /data/gg
 # ./ggsci
1> create subdirs
2> edit params mgr
PORT 7809
DYNAMICPORTLIST 7810-7909
AUTORESTART EXTRACT *,RETRIES 5,WAITMINUTES 3
PURGEOLDEXTRACTS ./dirdat/*,usecheckpoints, minkeepdays 3

3> edit  params  ./GLOBALS
CHECKPOINTTABLE WUXIHUISHAN_YUTIAOSHI.checkpoint

4> edit params rekafka
REPLICAT rekafka
sourcedefs /data/gg/dirdef/WUXIHUISHAN_YUTIAOSHI.USER_INFO
TARGETDB LIBFILE libggjava.so SET property=dirprm/kafka.props
REPORTCOUNT EVERY 1 MINUTES, RATE 
GROUPTRANSOPS 10000
MAP WUXIHUISHAN_YUTIAOSHI.*, TARGET WUXIHUISHAN_YUTIAOSHI.*;
```

编辑对应的kafka配置：
```bash
 # vi kafka.props
gg.handlerlist=kafkahandler
gg.handler.kafkahandler.type=kafka
gg.handler.kafkahandler.KafkaProducerConfigFile=custom_kafka_producer.properties
gg.handler.kafkahandler.topicMappingTemplate=togg
gg.handler.kafkahandler.format=json
gg.handler.kafkahandler.mode=tx
gg.handler.kafkahandler.format.includePrimaryKeys=true
gg.classpath=dirprm/:/opt/module/kafka_2.11-2.4.0/libs/*:/data/gg/:/data/gg/lib/*

 # vi custom_kafka_producer.properties
bootstrap.servers=192.168.1.157:9092
acks=1
compression.type=gzip
reconnect.backoff.ms=1000
value.serializer=org.apache.kafka.common.serialization.ByteArraySerializer
key.serializer=org.apache.kafka.common.serialization.ByteArraySerializer
batch.size=102400
linger.ms=10000
```

添加exttrail:
```bash
 # ./ggsci
1> add replicat rekafka exttrail /data/gg/dirdat/hs,checkpointtable WUXIHUISHAN_YUTIAOSHI.checkpoint
```

确认ogg的同步数据推送到了ogg BD:
```bash
- source :
 # ls -l /opt/ogg/dirdat/hs*
- dest: 
 # ls -l /data/gg/dirdat/hs*
```

## 3. destination install kafka
 - [How to install kafka](https://blog.csdn.net/csdnlihai/article/details/87787236)

1. 获取及安装：
```shell script
 # wget https://mirrors.cnnic.cn/apache/kafka/2.4.0/kafka_2.11-2.4.0.tgz --no-check-certificate
 # tar zxvf kafka_2.11-2.4.0.tgz
```

1. 编辑启动脚本-zookeeper:
```bash
 # cd /lib/systemd/system/ 
 # vim zookeeper.service 
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

1. 编辑启动脚本-kafka:
```bash
 # vim kafka.service 
[Unit]
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

1. 安装为service:
 ```bash
 # systemctl daemon-reload
 ```

1. zookeeper、kafka服务加入开机自启:
 ```bash
 # systemctl enable zookeeper
 # systemctl enable kafka
 ```

1. 使用systemctl启动/关闭/重启 zookeeper、kafka服务<br>
注：启动kafka前必须先启动zookeeper 。
 ```bash
 # systemctl start zookeeper
 # systemctl start kafka
 ```

### 常用kafka命令
```bash
 # ./bin/kafka-topics.sh --delete --bootstrap-server 192.168.1.157:9092 --topic togg
 # /opt/module/kafka_2.11-2.4.0/bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list 192.168.1.157:9092 --topic togg
 # bin/kafka-console-consumer.sh --bootstrap-server 192.168.1.157:9092 --topic togg --from-beginning
 # bin/kafka-topics.sh --list --bootstrap-server localhost:9092
 # bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
```

## 4. python with oracle in mac / linux
1. pip3 install cx_Oracle
1. 安装oracle instantClient
 - https://www.oracle.com/cn/technical-resources/topics/intel-macsoft.html
 - https://www.oracle.com/database/technologies/instant-client/macos-intel-x86-downloads.html
1. mac当前的user下进行配置。修改 user 的 .bash_profile. 在.bash_profile 文件中加入如下几行：
```bash
 # vi ~/.bash_profile
export ORACLE_HOME=/opt/oracle/instantclient
export DYLD_LIBRARY_PATH=$ORACLE_HOME
export LD_LIBRARY_PATH=$ORACLE_HOME
export NLS_LANG=AMERICAN_AMERICA.UTF8
export TNS_ADMIN=$HOME/etc
export PATH=$PATH:$ORACLE_HOME
```

1. linux
```shell script
 # rpm -ivh oracle-instantclient11.2-basic-11.2.0.4.0-1.x86_64.rpm 
 # vi ~/.bash_profile
export ORACLE_HOME=/usr/lib/oracle/11.2/client64
export DYLD_LIBRARY_PATH=$ORACLE_HOME
export LD_LIBRARY_PATH=/usr/lib/oracle/11.2/client64:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:$LD_LIBRARY_PATH
export NLS_LANG=AMERICAN_AMERICA.UTF8
export TNS_ADMIN=$HOME/etc
export PATH=$PATH:$ORACLE_HOME
 # source ~/.bash_profile
 # yum install  libaio-devel.x86_64 -y
```

1. source 以生效
```bash
 # source ~/.bash_profile
```

1. oracle 11 丢失的若干文件的处理
注意，把 oracle_home/lib 下 xxx.so.11.1 复制为 xxx.so
```bash
 # mkdir ~/lib
 # ln -s /opt/oracle/instantclient/libclntsh.dylib.11.2 ~/lib/
 # mkdir ~/lib
 # cp /opt/oracle/instantclient_11_2/{libclntsh.dylib.11.1,libnnz11.dylib,libociei.dylib} ~/lib/
 # mkdir -p /opt/oracle/instantclient_12_2/network/admin
```


1. 在python中配置环境变量
```python
os.environ["ORACLE_HOME"] = '/usr/lib/oracle/11.2/client64'
os.environ["DYLD_LIBRARY_PATH"] = '$ORACLE_HOME'
os.environ["LD_LIBRARY_PATH"] = '$ORACLE_HOME'
os.environ["NLS_LANG"] = "AMERICAN_AMERICA.UTF8"
# os.environ["TNS_ADMIN"] = '$ORACLE_HOME/network/admin'
os.environ["TNS_ADMIN"] = '$HOME/etc'
os.environ["PATH"] = '$PATH:$ORACLE_HOME'
```
