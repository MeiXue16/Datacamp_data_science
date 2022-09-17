import pandas as pd
#迭代
list1 = ['nana', 'miya', 'frango', 'frolin']
# for i in list1:
#     print(i)
iterate =iter(list1)    #创建迭代器
print(next(iterate))    #从迭代器里打印下一个:nana
print(next(iterate))    #miya

value = iter(range(3**100))  #创建迭代器
print(next(value))      #0
print(next(value))      #1

value2 =range(10,21)
print(value2)   #range(10, 21)
value2 =list(value2)
print(value2)   #[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

print(sum(value2))  #对列表内的值求和

#enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，
# 同时列出数据和数据下标，一般用在 for 循环当中。
# seasons = ['Spring', 'Summer', 'Fall', 'Winter']
# list(enumerate(seasons))
# [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
# list(enumerate(seasons, start=1))       # 下标从 1 开始
# [(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]

print(list(enumerate(list1)))

for i, x in enumerate(list1,start =1):
    print(i,x)

#zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，
# 然后用list()返回由这些元组组成的列表

list2 =[3,6,1,8,1,9,3,6,7,0]
list3 =['haha','nana','miya']
zip_list =list(zip(list2,list3))    #zip 按最短的列表数进行组合打包
print(zip_list)             #[(3, 'haha'), (6, 'nana'), (1, 'miya')]
print(zip(list1, list2,list3))     #<zip object at 0x000002A9DE829F80>

z1 =list(zip(list1,list2,list3))
for i,j,k in z1:
    print(i,j,k)

#解压 Unzip
zip1 =zip(list1, list2,list3)
print(*zip1)
print(*z1)      #结果与print(*zip1) 相同

r1, r2 =zip(*zip_list)      #解压
print(r1)
print(r2)                   #tuple
print(r2 == list3)          #false
print(list(r2) == list3)    #true

count ={}
#逐块迭代chunk, 当csv文件内容过大时,使用chunksize进行逐块读取
for chunkdata in pd.read_csv('./daten_file/daten1.csv',chunksize=10):
    for val in chunkdata['Nachname']:
        if val in count.keys():
            count[val] +=1
        else:
            count[val] =1
print(count)

#为大量的数据提取信息
def count2(csv_file, c_size, col):
    count={}
    for data in pd.read_csv(csv_file, chunksize= c_size):
        for val in data[col]:
            if val in count.keys():
                count[val] +=1
            else:
                count[val] =1
    return count
r3 =count2('./daten_file/daten1.csv', 20, 'zahlen')
print(r3)

# 列表理解和生成器
# 编写列表理解程序
square =[i**2 for i in range(10)]       #创建列表
print('square is:', square)

matrix =[[col for col in range(5)] for row in range(3)]     #创建3*5的矩阵
print(matrix[2][4])
for i in matrix:
    print(i)        #按行打印

list4 =[i for i in list1  if len(i)>4]      #条件打印
print(list4)

list5 =['frodo', 'samwise', 'merry', 'aragorn', 'legolas', 'boromir', 'gimli']
list6 =[i if len(i)>=7 else ''  for i in list5 ] #条件打印
print(list6)

#创建字典理解
dic1 ={i:len(i)   for i in list5}   #循环创建字典
print(dic1)

#创建生成器
#[] list对象不是一个迭代器iterator, 要iter(list1)将列表转换为迭代器后,才可以使用next()方法
#每个generator都是一个迭代器,反之不然
res =(i for i in range(31))  #generator object
print(res)
print(next(res))   #iterator的迭代方法next()
print(next(res))
for i in res:
    print(i)        #打印剩余的值

list7 =['cersei', 'jaime', 'tywin', 'tyrion', 'joffrey']
generator1 =(len(i) for i in list7)
for i in generator1:
    print(i)

def funk(listi):
    for i in listi:
        yield len(i)  #产生字符串的长度
for j in funk(list7):
    print(j)

daten1 =pd.read_csv('./daten_file/daten1.csv',nrows=25)
name =daten1['Vorname']
print(name)
res1 =[x for x in name[7:20] if x == ' Pia']  #条件打印
print(res1)

name = ['nana', 'miya', 'frolin','frango','eslameda','angela','brittel']
age =[16,20,21,29,49,50,28,34,10]
zip2 =zip(name, age)  #打包列表
dic2 =dict(zip2)        #转换为dictionary
print(dic2)

def list2dict(l1,l2):
    ziplist =zip(l1,l2)
    dic =dict(ziplist)
    return  dic

dic3 =list2dict(list1,list2)
print(dic3)

df =pd.DataFrame(list(dic3))
print(df.head())

with open('./daten_file/daten2.csv', mode= 'r',encoding='utf-8') as file:
    print(file.readline()) #返回第一行
    # print(file.readline())  #返回第二行
    # print(file.readline(10)) #返回第三行前10个字节

    count ={}
    for i in range(100):
        line =file.readline().split(',')    #把每行的内容按逗号拆分为列表
        firstcol =line[0]   #获取第一列的值
        if firstcol in count.keys():
            count[firstcol] +=1
        else:
            count[firstcol] =1
    print(count)

#编写一个生成器，以分块加载数据(2)
# 定义 read_large_file()
def readLargeFile(files):
    while True:
        line = files.readline()
        if not line:
            break
        yield line  #类似print, 但是yield 的作用就是把一个函数readLargeFile()变成一个 generator，带有 yield 的函数不再是一个普通函数，Python 解释器会将其视为一个 generator,可迭代,也就是可以使用next()函数

with open('./daten_file/daten2.csv', mode ='r', encoding='utf-8') as daten2:
    linecontent =readLargeFile(daten2)
    print('line1:',next(linecontent))
    print('line2:',next(linecontent))

counts={}
with open('./daten_file/daten2.csv', mode ='r', encoding= 'utf-8') as daten3:
    for line in readLargeFile(daten3):  #readLargeFile(daten3)是可迭代对象
        row =line.split(',') #将每行内容转换为列表
        secondcol =row[1]
        if secondcol in counts.keys():
            counts[secondcol] +=1
        else:
            counts[secondcol] =1
print(counts)


#写一个迭代器来分块加载数据(1)
daten4 =pd.read_csv('./daten_file/daten2.csv', chunksize=10) #按每10行为一块，分块读取daten2.csv的数据,迭代器
print(next(daten4))     #0-9行
print(next(daten4))     #10-19行

#写一个迭代器来分块加载数据(2)
daten5 =pd.read_csv('./daten_file/daten1.csv', chunksize=20, header=0)  #header=0第一行为标题/列名
daten_20rows =next(daten5) #前20行保存为daten_20rows
print('daten:',daten_20rows)
# new_daten =[]
# for i in daten_20rows:
#     line=i.split(',')   #发现此文件的.columns没有分隔开，因此先将字段按逗号分割为列表，再转换为dataframe
#     new_daten.append(line)
# print('daten:',new_daten)
#
# new_daten =pd.DataFrame(new_daten) #将列表转换为dataframe
# print('列名:',new_daten.columns) #显示dataframe列名
# print(new_daten)
daten_cc =daten_20rows[daten_20rows['Vorname']=='Anne']
print('Name:',daten_cc)

ccpaar =list( zip(daten_20rows['Vorname'],
            daten_20rows['Nachname']))
print(ccpaar)


#写一个迭代器来分块加载数据(3)
daten6 =pd.read_csv('./daten_file/daten3.csv',chunksize=100)
df2= next(daten6)
#print(df2.iloc[0])
print(df2.columns)
df_cc =df2[df2['CountryCode'] == 'CSS']
print(df_cc)

df_zip =list( zip(df2['Total Population'], df2['Urban population (% of total)']))
print(df_zip)

df2.drop(columns='Unnamed: 5',inplace=True) #删除某列
df2['new column']= [int(x[0] * x[1] *0.01) for x in df_zip]  #保留3位小数: round(x, 3)
print(df2)

import matplotlib.pyplot as plt

#df2.plot(kind='scatter', x='Year', y='new column')
plt.scatter(x= df2['Year'], y= df2['new column'])   #画图
#plt.show()

#写一个迭代器来分块加载数据(4)
daten7 =pd.read_csv('./daten_file/daten3.csv',chunksize=100)

df3 =pd.DataFrame()     #新建一个空的dataframe

#迭代/循环
for datas in daten7:
    df_ceb =datas[ datas['CountryCode']== 'CEB' ]
    df_zip2 =list( zip(df_ceb['Total Population'],
                 df_ceb['Urban population (% of total)']))
    df_ceb['new column']=[int(x[0] *x[1] * 0.001) for x in df_zip2]
    df3 =df3.append(df_ceb)
print(df3)
plt.figure()
plt.scatter(x=df3['Year'], y= df3['new column'] )
#plt.show()

#写一个迭代器来分块加载数据(5)
def plot_daten(file, country_code):
    daten8 =pd.read_csv(file, chunksize=100)
    df4 =pd.DataFrame()

    for datas1 in daten8:
        df_ceb2 =datas1[ datas1['CountryCode']==country_code]
        df_zip3 =list( zip(df_ceb2['Total Population'],
                           df_ceb2['Urban population (% of total)']))
        df_ceb2.drop(columns='Unnamed: 5', inplace=True)
        df_ceb2['new']= [int(x[0]* x[1] *0.001) for x in df_zip3]
        df4 =df4.append(df_ceb2)

    plt.figure()
    plt.scatter(x= df4['Year'], y= df4['new'])
    plt.show()

plot_daten('./daten_file/daten3.csv', 'CEB')
plot_daten('./daten_file/daten3.csv', 'ARB')



