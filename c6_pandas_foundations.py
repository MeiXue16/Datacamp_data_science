# 数据采集和检查 Datenerhebung und Prüfung
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#导入csv数据为dataframe
df =pd.read_csv('./daten_file/dob_job_application_filings_subset.csv')
print(df.head())
print(df.info())

# 提取一列作为数组
np_vals =df['ExistingNo. of Stories']
print(type(np_vals))    #<class 'pandas.core.series.Series'>

# 创建新的以10为基数的对数值 数组：
np_vals_log10 =np.log10(np_vals)
print(np_vals_log10)

# 创建新的以10为基数的对数值 dataframe:
# df_log10 =np.log10(df)          #前提是df中的数据都为numeric类型
# print(df_log10.head())

#  利用Zip列表 建立dataframe

zipped =list(zip(df.Borough, df['Job Status Descrp']))
# print(zipped)

# 把zipped列表建立成DataFrame：
# df1 =pd.DataFrame(zipped)
df1 =pd.DataFrame(zipped, columns=['Borough','Job Status Descrp'])
print(df1.head())

#修改全部列名：
df1.columns =['artist', 'descrip']
#在原表上（inplace= True）修改某列列名：
df1.rename(columns={'artist': 'art.'},inplace= True)
print(df1.head())

#用broadcasting建立数据框架
# 创建字典
data1 ={'state':['PA','USA'], 'city':['Jena','Newyork']}
#用字典创建dataframe,定义数据类型
df2 =pd.DataFrame(data1, dtype ='category')
print(df2)

# 导入csv文件并重命名列名
# header= 0 数据的第一行作为标题行，names=list('abcde') 修改标题行为a b c d e
# header =None 指数据没有标题行
df3 =pd.read_csv('./daten_file/daten1.csv',header= 0, names=list('abcde'))
print(df3.head())

# 数据的第 3 行作为标题行,第 3 行之前的内容不读取，
# #号后的内容为注释，如果在一行的开头找到，则该行将被完全忽略
# 分隔符为逗号
df4 =pd.read_csv('./daten_file/daten1.csv', header= 3, comment='#',delimiter=',')
print(df4.head())

# 将清理过的DataFrame保存到一个没有索引的CSV/excel文件中
df4.to_csv('./daten_file/daten9.csv', index = False)
df3.to_csv('./daten_file/daten10.xlsx', index= False)

#画图，自动以index为 x-axis, df3['e']为 y-axis
df3['e'].plot()
#plt.show()

#画图, 一张画布上同时画两个图
plt.figure()
df5 =pd.read_csv('./daten_file/daten3.csv',header=0, names=list('abcdef'))
print(df5.head())
df5['d'].plot()
df5['e'].plot()
#plt.show()


#Exploratory data analysis 探索性数据分析

#画图
#两列数据
y_columns=['d','e']
#一张图上画两条折线,并命名两条线分别为'price1','price2'
df5.plot(x='c', y= y_columns, label= ['price1','price2'])
plt.title('monthly prices')
plt.xlabel('year')
plt.ylabel('price')
# 生成图例， 位置为'upper right'
plt.legend(loc ='upper right')
#plt.show()

# pandas散点图
df5.plot(kind='scatter', x= 'c', y ='d')
plt.xlabel('year')
plt.ylabel('prices')
plt.title('happy')
#plt.show()

#pandas箱形图
cols =['e', 'd']
df5[cols].plot(kind='box', subplots= False, label =['cc','dd'], showmeans =True)
# 等价于
plt.figure()
#箱形图 横坐标标签 labels =('cc','dd')
plt.boxplot([df5.e, df5.d],  labels =('cc','dd'), showmeans =True)
# plt.show()

#pandas hist, pdf and cdf
# 这将使绘图格式化（新建n*m的画布），使它们出现在不同的行中
fig, ax =plt.subplots(nrows =2, ncols=1)

#画法1
df5.e.plot(ax =ax[0], kind='hist',  bins=30,range =(0,50), rwidth =0.8)
# plt.show()
#画法2
ax[1].hist(df5['e'], bins=20, range=(0,60),rwidth=0.8, orientation='vertical')


#描述统计量 Deskriptive Statistik

# min/max 几种求法
print(df5.e.min())
print(df5['e'].max())
print(np.min(df5.e))

# 均值
plt.figure()
df6 =pd.read_csv('./daten_file/daten4.csv', header=None, names=list('abcdefghi'))

#展示所有列的均值，并画折线图
mean1 =df6.mean(axis ='columns')
mean1.plot()
#plt.show()
#某一列的均值, 以下求法等价
print(df6['a'].mean())
print(df6.a.mean())
print(np.mean(df6['a']))

#中位数与平均数  Median vs mean
#输出列e的所有描述统计量
print(df6.e.describe())

df6.e.plot(kind='box')
# plt.show()

#非空单元格计数：count
print(df6['e'].count())
print(df5.a.count())

#分类计数
print(df5.c.value_counts(dropna =True))

# Quantiles 分位数
# 打印所有列的第5和第95百分位数
print(df6.quantile([0.05, 0.95]))

#打印列e的百分位数
print(df6.e.quantile([0.05,0.95]))

#标准差 std. deviation
print(df6.e.std(), df6.std())

#筛选和计数 Filtering and counting
#筛选 e列中等于23的值 对应的行
e1 = df6[df6.e == 23]
e2 = df6.loc[df6['e'] == 23]
print(e1 == e2)     #返回一行bool值： True

#这一行e1的均值/标准差
print(e1.mean(), e1.std())

#画图
fig, ax =plt.subplots(nrows=2, ncols=2)
# 单行数据不能画图
# ax[0,0].boxplot(df6.loc[df6.e == 23], vert =True, showmeans=True)
# ax[0,1].plot( x= df6[df6.c == 8], y= df6.loc[df6.e == 23])

# 多行数据 按列画图
df6.loc[df6.e == 23].plot(ax= ax[0,0])
# plt.show()


#在pandas中的时间序列

#日期时间的切分

# 转换数据类型
# df6.c = df6.c.astype('datetime64')
# 将某列转换成一个日期时间对象
time_format = '%Y-%m-%d %H:%M'
my_datetimes = pd.to_datetime(df6['c'], format= time_format)

# 构建一个时间序列，索引为日期时间
time_series =pd.Series(df6.d, index =my_datetimes)
# print(time_series)

# 打印'1997-10-11 21:00'对应的值
# print(time_series.loc['1997-10-11 21:00'])
# 打印'1997-10-11 21:00' 至 '2000-10-20 22:30'的值
# print(time_series.loc['1997-10-11 21:00' : '2000-10-20 22:30'])


#重新编制索引
# 重新设置索引而不使用填充方法:
# 创建索引为0-99的时间序列
t1 =pd.Series(df6.d, index= range(100))
# 如果新添加的索引没有对应的值，则默认为nan. 多出来的index，可以使用fill_value=  填充 或 使用原本序列中的值向前填充method='ffill'
# 如果减少索引，就相当于一个切片操作。
t2 =t1.reindex( index =range(200), fill_value= 10)
print('t1:',t1)
print('t2:',t2)
# method='ffill'/ ''bfill' / 'nearest'用于填充重新索引的 DataFrame 中的孔的方法. 这仅适用于具有单调递增/递减索引的 DataFrames/Series。
# 最后两行的值并没有被填补
t3 =t1.reindex(index =range(28), method ='bfill')
print('t3:',t3)

sum1 =t2+ t3
print(sum1)

#重新采样时间序列数据

# 向下采样和执行聚合 Down-Sampling und Aggregation
# 下采样是将一个时间序列数据集重新采样到一个更大的时间框架。例如，从几分钟到几小时，从几天到几年。结果的行数将减少，
# 并且可以使用mean()、min()、max()、sum()等聚合值。
# DataFrame.resample(rule, axis=0, closed=None),这个DataFrame的索引列是日期时间
# rule: DateOffset, Timedelta or str 该对象必须具有类似日期时间的索引（DatetimeIndex、PeriodIndex或TimedeltaIndex）
# 例如 t1.resample('2H') 将t1向下采样到2小时的容器中(每隔两小时一条记录)
index = pd.date_range('1/1/2000', periods=9, freq='2H') #起始日期时间为1/1/2000，每2小时一条数据(也可以写为'2T')，共9条数据
t4 =pd.Series(range(9),index=index)     #时间序列的索引为index
# print(t4)
print(t4.resample('3H', label= 'left').sum())          #按3小时(H/h)的倍数向下采样，并将落入容器中的时间戳的值相加,默认label='left'容器的左边缘

# closed='right',将时间戳的右侧设为闭区间，即index不能超出原有时间戳的右边界
print(t4.resample('4h', label='right',closed='right').agg([min,max,sum])) #按4小时(H/h)的倍数down sampling, 落入容器中的时间戳的值求最小，最大，相加值（['min','max','sum']加引号效果一样）

#设置时间索引,频率为天d
index2 =pd.date_range('1/1/2010',periods=100, freq='d')
#新建时间序列
t5 =pd.Series(range(100), index=index2)
print(t5.head())
#向下采样,按月采样,默认右边缘
ds1 =t5.resample('m', label= 'right').agg(['count', 'mean','sum'])
print(ds1)

#新建dataframe
df7 =pd.DataFrame(np.arange(0,1000,1).reshape(100,10), index=index2, columns=list('abcdefghij'))
#筛选df7的 a列 2月的值
print(df7['a']['2010-02'])
#筛选b列 2-3月的值
feb_march =df7.b.loc['02/2010':'03/2010']
print(feb_march)

#筛选df7的 2月的行(所有列)
feb =df7.loc['2010-2']
print(feb.head())
#筛选df7的 2月3号到4月1号的行
feb2 =df7.loc['2010-02-03': '2010-04-01']
print(feb2.head())

#下采样，2月每周的最高和最低温
feb_max =feb.resample('w').max()
print(feb_max)
feb_agg =feb.resample('w').agg([min,max])
print(feb_agg)

# 应用每3天窗口的移动平均值：平滑的(每3天取一个均值)
# index 0,1 为NaN，是因为它们前面都不够3个数，
# index2 的值就是（index0+index1+index2 ）/3
# index3 的值就是（ index1+index2+index3）/3
# center: 布尔型，默认False，居右
# min_periods：每个窗口最少包含的观测值数量，小于这个值的窗口结果为NA。值可以是int，默认NaN。offset情况下，默认为1。
# axis: 默认为0，即对列进行计算
# closed：定义区间的开闭,默认是左开右闭的即right.可以根据情况指定为'left', 'both'等。
smooth =feb_march.rolling(window=3, center= False).mean()

#创建dataframe(连接两个series)
combined =pd.DataFrame({'unsmoothed':feb_march, 'smoothed':smooth})
print(combined.head())
plt.figure()
#画图，两列数据就是两条折线，x轴默认为索引
combined.plot()
# plt.show()


#Method chaining and filtering
#从列名中去除多余的空格
df6.columns = df6.columns.str.strip()
#去除某列值的多余空格
df6.a =df1['art.'].str.strip()

#筛选/提取符合某些条件的数据
#str.contains(pat='***')返回bool列
# pat: 字符序列或正则表达式。
manhattan=df1['art.'].str.contains('MANHATTAN')
# print(manhattan)
# 筛选'art.'列包含'MANHATTAN'的所有行数据，等价于df1.loc[manhattan ==1(True)]
manh =df1.loc[manhattan]
# print(manh)

index3 = pd.date_range(start='1998-01-01', periods=6310, freq= 'D')
#设置索引为时间日期
manh = manh.set_index(index3)
print(manh.head())
#下采样, 计数每个月的数据个数
count_manh =manh['descrip'].resample('m').count()
print(count_manh)
# 生成count_manh的汇总统计数据
print(count_manh.describe())


# 遗漏值和插值 Missing values and interpolation

# 将count_manh的索引重置为index4，然后使用线性插值来填充NaN
index4 =pd.date_range('1998-01-01', periods=10000,freq='D')
# df.interpolate(method='linear', axis=0, limit=None, inplace=False, limit_direction=None, limit_area=None, downcast=None, **kwargs)
# method: 'linear'(默认),'time', 'index', 'pad', 'nearest', 'polynomial'...
# limit: 要连续填充的NaN的最大数量。必须大于0。
count_manh2 =count_manh.reindex(index4).interpolate(method ='linear')
print(count_manh2.tail())

# 计算count_manh和count_manh2的绝对差异
diff =np.abs(count_manh2 -count_manh)
#生成diff的汇总统计数据
print(diff.describe())

#时区和转换
#筛选符合条件的行数据
manh2 =df1.loc[df1['art.'] == 'MANHATTAN']
#设置索引
manh2 =manh2.set_index(index3)
#等价于
manh2.set_index(index3,inplace=True)
#新建列‘date’
manh2.loc[:,'date']=np.arange(0,6310,1)
manh2['date'] =pd.to_datetime(range(6310), unit='D',origin=pd.Timestamp('1990-01-01'))
print(manh2.date.head())
#新建列‘time’
time1 = pd.timedelta_range('0:30:00',periods=6310, freq= 'h')
manh2.loc[:,'time'] =time1
print(manh2.head())

#组合索引列和某一列构成一个新的时间序列
series1 =pd.to_datetime(manh2.index + manh2['time'])
#组合两列新建列构成一个新的时间序列
series2 =pd.to_datetime(manh2['date'] + manh2['time'])
print(series1.head())

# 将时间本地化为美国/中部
series2_us =series2.dt.tz_localize('US/Central',nonexistent='shift_forward')
print(series2_us.head())

# 将时间本地化为欧洲/华沙
series2_europe =series2.dt.tz_localize('Europe/Warsaw' ,nonexistent='shift_backward')
print(series2_europe.head())

#选取索引为1月到3月的温度列画图
df.temperature['01-2010':'03-2010'].plot()



