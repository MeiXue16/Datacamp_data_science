#在Python中使用关系型数据库 relational databases
#创建一个数据库引擎database engine

from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
# engine1 =create_engine('sqlite://chinook.sqlite')   #数据库 URL 的典型形式是 dialect+driver://username:password@host:port/database
#Dialect names include the identifying name of the SQLAlchemy dialect, a name such as sqlite, mysql, postgresql, oracle, or mssql.
# default
#engine = create_engine('mysql://guest:Guest.618@%/market')

engine = create_engine('mysql://root:whdhd.cnm1314@localhost/market')

# # mysqlclient (a maintained fork of MySQL-Python)（MySQL-Python的一个维护性分叉）
# engine = create_engine('mysql+mysqldb://root:1314@localhost/hrs')
#
# # PyMySQL
# engine = create_engine('mysql+pymysql://root:1314@localhost/hrs')
table_names =engine.table_names()
print(table_names)

import pandas as pd
connect1 = engine.connect()     # 打开引擎连接
query1 =connect1.execute('select * from masterliste')       #执行sql查询
connect1.close()                #关闭连接

print(query1)           #<sqlalchemy.engine.cursor.LegacyCursorResult object at 0x0000024C8CBCE170>
df1 =pd.DataFrame(query1.fetchall())        #将查询结果保存入dataframe
print(df1.head())

#自定义SQL查询的 "你好世界
# 在上下文管理器中打开引擎
#执行查询，并将结果保存到DataFrame
with engine.connect() as connect2:
    query2 =connect2.execute('select Firmenname as name,Homepage as "website" from masterliste')
    df =pd.DataFrame(query2.fetchmany(size=3))      #获取前三行
    #df.columns =query2.keys()          #dataframe列名=查询键名， 没有这行声明，结果也是一样的

print(len(df))      #3
print(df.head())

#使用SQL的WHERE过滤你的数据库记录
with engine.connect() as con3:
    # sql ="select * from masterliste where Firmenname like %s oder by Firmenname; "
    # str1 =['%s%%' % 'F']
    # query3 =con3.execute(sql, str1) #不要 F开头的Firmenname
    query4 =con3.execute('select * from masterliste where Firmenname <> "JenaGen GmbH" order by Firmenname')
    df2 =pd.DataFrame(query4.fetchall())

print(df2.head())

df3 =pd.read_sql_query("select * from masterliste", engine)     #执行查询并将记录存储在DataFrame中
print(df3.head())

with engine.connect() as con4:
    df4 =pd.read_sql_query('select * from masterliste where Homepage <> "www.vacom.de" order by Firmenname ', engine)
print(df4.head())












