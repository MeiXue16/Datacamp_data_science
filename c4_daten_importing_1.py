#导入txt文件
import json

file_a =open('hello.txt', mode='w')     #导入模式为写入write
file_a.write('hello\nworld!\n')    #写入string，write时， 只能写入二进制或字符串

name =['nana', 'saber', 'frolin']   #字典，列表，数字都不能直接写入文件中
json.dump(name, file_a)         #将列表name 按Json格式转换为str后 保存入 file_a,序列化

file_a =open('hello.txt', mode='r')     #导入模式为读取read
print(file_a.read())                    #读取文件内容

file_a.close()              #关闭文件
print(file_a.closed)        #检查文件是否关闭

#上下文管理器 kontext manager
with open('hello.txt', mode='r', encoding='utf-8') as file_b:
    print('first line: ',file_b.readline())    #打印第一行
    print('second line: ',file_b.readline())    #打印第二行


#Using NumPy to import flat files
import numpy as np
import matplotlib.pyplot as plt
file_c ='./daten_file/daten4.csv'

arr1 =np.loadtxt(file_c, delimiter=',')     #将csv文件加载为数组,读取内容为数字
print(type(arr1))                       #<class 'numpy.ndarray'>

row21 =arr1[21, 0:]     #选取某行数据
#print(row21)
row21_sq =np.reshape(row21,(3,3)) #将这行数据变成3*3的数组
print(row21_sq)

plt.imshow(row21_sq, cmap='Greys', interpolation='nearest')              #将数组展示为图像
#plt.show()

file_d ='./daten_file/daten5.TXT'
arr2 =np.loadtxt(file_d, delimiter='\t',skiprows=1)          #将txt文件加载为数组,分隔符为tab,读取内容为数字,因此跳过第一行
print(arr2)

arr3 =np.loadtxt('./daten_file/daten1.csv', delimiter=',',dtype=str, encoding='utf-8')  #将csv文件加载为数组，数据类型为str
print(arr3[0])

arr4 =np.loadtxt('./daten_file/daten4.csv',delimiter=',', dtype=float,skiprows=1) #数据类型为float, 跳过第一行
print(arr4[10])

plt.figure()
plt.scatter(arr4[:,0], arr4[:,2])
plt.xlabel('time(min)')
plt.ylabel('percentage of larve')
#plt.show()

#混合数据类型
file_e ='./daten_file/daten3.csv'
arr5 =np.recfromcsv(file_e, delimiter=',', names=True, dtype=None)  #names=True：跳过数据标题行/第一行， 允许多种数据类型
print(arr5[:3])     #打印前三行


#Using pandas to import flat files as DataFrames (1)
import pandas as pd

daten1 =pd.read_csv('./daten_file/daten3.csv')  #将文件读入一个DataFrame中
print(daten1.head())        #打印前5行

daten2 =pd.read_csv('./daten_file/daten3.csv', nrows=20, header=None)       #设置没有表头，将表头作为数据行的第一行
print(daten2.head())        #打印前5行

data_arr= daten1.values        #将dataframe格式的数据转换为数组
print(type(data_arr))       #<class 'numpy.ndarray'>

daten3 =pd.read_csv('./daten_file/daten6.txt', sep='\t', comment='#',na_values=['Nothing'])     #把tab作为分隔符，#作为注释
print(daten3)
print(daten3.columns)

plt.figure()
pd.DataFrame.hist(daten1[['Total Population']])
plt.show()

