python读取oracle 

1. pip3 install cx_Oracle
2. https://www.oracle.com/cn/technical-resources/topics/intel-macsoft.html
 install oracle instantClient
 https://www.oracle.com/database/technologies/instant-client/macos-intel-x86-downloads.html
 
 
 mac当前的user下进行配置。修改 user 的 .bash_profile. 在.bash_profile 文件中加入如下几行：

    # oracle

    export ORACLE_HOME=/opt/oracle/instantclient

    export DYLD_LIBRARY_PATH=$ORACLE_HOME

    export LD_LIBRARY_PATH=$ORACLE_HOME

    export NLS_LANG=AMERICAN_AMERICA.UTF8

    export TNS_ADMIN=$HOME/etc

    export PATH=$PATH:$ORACLE_HOME

source~/.bash_profile

mkdir ~/etc

            touch tnsnames.ora
 orcl =
 (DESCRIPTION = 
   (ADDRESS_LIST =
     (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.1.88)(PORT = 1521))
   )
 (CONNECT_DATA =
   (SERVICE_NAME = orcl)
 )
)

mkdir ~/lib
ln -s /opt/oracle/instantclient/libclntsh.dylib.11.2 ~/lib/
mkdir ~/lib
cp /opt/oracle/instantclient_11_2/{libclntsh.dylib.11.1,libnnz11.dylib,libociei.dylib} ~/lib/
mkdir -p /opt/oracle/instantclient_12_2/network/admin


        os.environ["ORACLE_HOME"] = '/opt/oracle/instantclient'
        os.environ["DYLD_LIBRARY_PATH"] = '$ORACLE_HOME'
        os.environ["LD_LIBRARY_PATH"] = '$ORACLE_HOME'
        os.environ["NLS_LANG"] = "AMERICAN_AMERICA.UTF8"
        # os.environ["TNS_ADMIN"] = '$ORACLE_HOME/network/admin'
        os.environ["TNS_ADMIN"] = '$HOME/etc'
        os.environ["PATH"] = '$PATH:$ORACLE_HOME'
