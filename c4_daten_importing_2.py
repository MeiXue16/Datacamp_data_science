#Loading a pickled file 二进制文件
#json:将python中的数据(str/ list / tuple/ list/ dict/ int/ float/ bool/ None)转换为对应的json类型
#pickle:将python中任意对象转换为二进制

# dump - 将Python对象按照JSON/pickle格式 序列化到 文件fs中 serialization
# dumps - 将Python对象 序列化为JSON/pickle格式的 数据 serialization
# load - 将文件中的JSON/pickle格式数据 反序列化成 对象 deserialization
# loads - 将JSON/pickle格式的数据 反序列化成 对象 deserialization
import pickle
with open('./daten_file/daten6.pkl','wb') as file:  #注意：对于pickle格式的文件一定是binary的，因此模式为wb/rb
    # x='hello, I am Mei.'
    # file.write(pickle.dumps(x))     # write函数只能写入string/binary, 将x序列化为二进制后再写入文件
    # list1 =[3,5,4,1,4,6,7,8,9]      #列表，字典，数字都不能直接写入文件中
    # pickle.dump(list1, file)        #将list1写入文件file中
    dic1 ={'age':16, 'name':'mei', 'adress':'jena'}
    pickle.dump(dic1, file)         #只能写入第一次写入的内容，多次写入无效

with open('./daten_file/daten6.pkl',mode= 'rb') as file1:   #read binary
    d = pickle.load(file1)          #将文件中的内容 反序列化（加载load）为对象
print(d)
print(type(d))      #<class 'dict'>


import json
with open('./daten_file/daten7.txt', mode='w') as file2:    #文件格式也可以为.json
    y= 'welcome to my world!'
    list2 =[3,6,7,8,1,300,20,12]
    #file2.write(json.dumps(y))      #将string序列化为json格式的数据.读取（load）数据时只能读取写入一次的内容，写入两次读取时会报错。
    json.dump(list2 , file2)        #将list2序列化为json格式的文件

with open('./daten_file/daten7.txt',mode='r') as file3:
    d2 = json.load(file3)
print(d2)


# 在Excel文件中列出工作表
import pandas as pd
import openpyxl
x1 =pd.ExcelFile('./daten_file/daten.xlsx')
print(x1.sheet_names)       #输出excel文件的所有工作表表名['Tabelle1', 'tab2']

df1 =x1.parse('Tabelle1')   # 按名称将工作表载入dataframe
print(df1.head())

df2 =x1.parse(1)    #按索引将第2个工作表载入dataframe
print(df2.head())

#自定义你的excel的导入
df3 =x1.parse(0,parse_cols=[7], skiprows=[0], names=['country']) #导入/解析x1的第一个工作表 (的第**列 parse_cols 不起作用)，跳过第一行，重命名为country
print(df3.head())

df4 =x1.parse(0, skiprows=[0], names=['a','b','c','d']) #解析第一个工作表并重命名各列
print(df4.head())

#导入SAS文件并转换为dataframe
from sas7bdat import SAS7BDAT as st
import matplotlib.pyplot as plt
with st('sales.sas7bdat') as file4:
    df_sas =file4.to_data_frame()
print(df_sas.head())

pd.DataFrame.hist(df_sas[['P']])
plt.ylabel('count')
plt.show()

#导入Stata文件并转换为dataframe
df5 =pd.read_stata('hello.dta')
print(df5.head())

plt.figure()
pd.DataFrame.hist(df5[['disa10']])
plt.xlabel('extent')
plt.yalabel('number of countries')
plt.show()

#使用h5py 导入hdf5文件
import numpy as np
import h5py
dic2 =h5py.File('./daten_file/ligo.hdf5', 'w')
print(type(dic2))       #dictionary
for key in dic2.keys():
    print(key)

starin =dic2['strain']['starin'].value
num_samples =10000
time =np.arange(0,1, 1/num_samples) #start end step
plt.figure()
plt.plot(x= time, y= starin[:num_samples])
plt.xlabel('GPS time')
plt.ylabel('strain')
plt.title('title')
plt.show()

#导入 matlab文件
import scipy.io
mat = scipy.io.loadmat('hello.mat')
print(type(mat))    #dictionary
print(mat.keys())
print(type(mat['countryno.']))  #array
print(np.shape(mat['countryno.']))

mat2= mat['countryno.'][25,5:] # 对数组进行子集并绘制
plt.figure()
plt.plot(mat2)
plt.show()



