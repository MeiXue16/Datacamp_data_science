# 探索你的数据

import pandas as pd

# Read the file into a DataFrame: df
df = pd.read_csv('./daten_file/dob_job_application_filings_subset.csv',low_memory=False)
print('head: ',df.head())        #打印前五行
print('tail: ', df.tail())        #打印最后五行
print('shape: ',df.shape)         #打印数据结构df的形状 shape:  (12846, 82) 行，列

# print('columns:', df.columns)   #打印df的列名

print('info: ',df.info())           #打印数据类型，行数，列，列名，列的数据类型

# 分类数据的频数统计
# 打印'Borough'列的值计数
print(df['Borough'].value_counts(dropna = False))    #分类计数 MANHATTAN 6310， BROOKLYN  2866，QUEENS 2121...

# 打印'State'列的值计数
print(df['State'].value_counts(dropna = False))

#用直方图显示单一变量的情况:直方图只适用于numeric类型的数据
import matplotlib.pyplot as plt
plt.figure()
df['Existing Height'].plot(kind= 'hist',bins=20, range=(0,1000), rwidth= 0.8)

plt.figure()
# normed=True 是频率图，默认是频数图.
# range=(0,100) 筛选数据范围，默认是最小到最大的取值范围.
# orientation=u'vertical' 水平或垂直方向
# rwidth=0.8  柱子与柱子之间的距离，默认是0
# log=False
plt.hist(df['ExistingNo. of Stories'], bins=20,range=(0,80), orientation=u'vertical',rwidth=0.8  )

#保存图片：
# Get the current figure.获取当前图片 gcf()
fig1 = plt.gcf()

#设置图片尺寸
fig1.set_size_inches(7.2, 4.2)

#保存图片
fig1.savefig('./daten_file/fig1.png',dpi = 100)

#plt.show()

#柱状图、饼图、箱线图（箱型图）是另外 3 种数据分析常用的图形，主要用于分析数据内部的分布状态或分散状态。
# 其中箱线图（箱型图）的主要作用是发现数据内部整体的分布分散情况，包括上下限、各分位数、异常值。

# 箱型图 x=[df[],df[],df[],...], vert:垂直显示， showmeans:显示均值
plt.figure()
plt.boxplot([df['ExistingNo. of Stories'], df['Proposed No. of Stories'], df['Existing Height']] ,
            labels =('ExistingNo.','ProposedNo.','height'), vert= True, showmeans= True)
# plt.show()

#散点图
plt.figure()
plt.scatter(x= df['ExistingNo. of Stories'], y=df['Existing Height'], c='red' )
#plt.show()


#Aufräumen von Daten für die Analyse 整理数据以便分析

# pandas.melt(frame, id_vars=None, value_vars=None, var_name=None, value_name='value', col_level=None)
# melt: 宽数据 => 长数据
# frame:要处理的数据集。
# id_vars:索引列，也是不需要被转换的列。
# value_vars:需要转换的列名，如果除索引列外全部需要转换，这个字段可以不写。
# 如果只有一列col1需要被转换，那么就会产生一列variable(值全都是col1),一列value(col1的值)
# 如果col1和col2需要被转换，就意味着col1和col2会被合并成一列
# var_name和value_name是自定义设置对应的variable和 value列名。
# col_level :如果列是MultiIndex，则使用此级别。

df2 =pd.read_csv('./daten_file/daten8.csv', nrows=10, sep=';')
df2_melt =pd.melt(df2, id_vars=['quality'], value_vars=['fixed acidity', 'volatile acidity'])
print(df2_melt.head())

#根据透视表df2_melt的variable列的第一个单词 创建新列‘gender’
df2_melt['gender'] =df2_melt.variable.str[0]
#根据透视表df2_melt的variable列的包括第二个单词后的所有单词 创建新列‘age_group’
df2_melt['age_group']= df2_melt.variable.str[1:]
print('new df2_melt:\n', df2_melt.head())


melt2 =pd.melt(df2, id_vars=['pH','density'], value_vars=['alcohol','sulphates'], var_name='Inhaltsstoffe', value_name='Value')
print(melt2.head())

#用.split()和.get()来分割一列

#新建一列'str_split'， 内容为 Inhaltsstoffe列 的值 根据 'o'符号分割开，
# 例如 Inhaltsstoffe列 的 alcohol => [alc, h, l]
melt2['str_split'] =melt2.Inhaltsstoffe.str.split('o')

#新建一列'type'， 内容为 'str_split'列表的第一个元素
melt2['type'] =melt2.str_split.str.get(0)

#新建一列'country'， 内容为 'str_split'列表的第二个元素
melt2['country']= melt2.str_split.str.get(1)

print('new melt2 :\n', melt2.head())


#Pivot data 透视数据
# Dynamische Anordnung der Daten und Aggregation nach Kategorien
#pivot_table(data, values=None, index=None, columns=None,aggfunc='mean', fill_value=None, margins=False, dropna=True, margins_name='All')
#pivot_table 有四个最重要的参数index(行标签)、values（值）、columns（列标签，不是必须字段）、aggfunc=[np.sum,np.mean]（设置我们对数据聚合时进行的函数操作），margins= False/True(将所有行/列相加（例如，小计/大计）)
import numpy as np
df3 =pd.read_csv('./daten_file/daten3.csv')
pivot1 = df3.pivot_table(index=['CountryName', 'CountryCode'],
                         values=['Total Population','Urban population (% of total)'],
                         aggfunc=[np.mean,np.sum] )

# print('pivot1:\n', pivot1.head())

#将dataframe存入excel中
pivot1.to_excel('pivot1.xlsx')

#重新设置透视表行标签
pivot2 =pivot1.reset_index('CountryCode')
# print('pivot2: \n', pivot2.head())




