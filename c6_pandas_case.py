import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#第一行作为表头，修改表头列名为abcd
df =pd.read_csv('./daten_file/weather_data.csv',header=0,names=list('abcd'))
print(df.head())

#把所有行都当成数据，没有标题行
df_noheader =pd.read_csv('./daten_file/weather_data.csv',header=None)
print(df_noheader.head())

column_labels='Temperature,DewPoint,Pressure,Date'
#把str拆分转换为list: .split('*')
col_list =column_labels.split(',')
#修改列标签/列名
df.columns =col_list

# 删除相应的行/列
# DataFrame.drop(labels=None, axis=0, index=None, columns=None, level=None, inplace=False, errors='raise')

# 返回删除两列后剩余的列
df_dropped =df.drop(columns=['DewPoint','Pressure'])
df_dropped2 =df.drop(['DewPoint','Pressure'], axis=1)
# print(df_dropped==df_dropped2)      # true列表

#返回删除某行后剩余的行
df_d1 =df.drop(index=[0,1,2])
df_d2 =df.drop([0,1,2], axis=0)
print((df_d1 ==df_d2).head())       # true列表

#清理和整顿日期时间数据
#将日期列转换成字符串
df_dropped['Date'] =df_dropped['Date'].astype('str')

#新建一列'useless'，将Date列的内容按空格分割成list列
df_dropped['useless'] =df_dropped.Date.str.split(' ')

#新建一列‘date’,获取'useless'列的列表中第1个元素
df_dropped['date'] = df_dropped.useless.str.get(0)
#新建一列‘time’,获取'useless'列的列表中第2个元素
df_dropped['time'] =df_dropped.useless.str.get(1)

# 将前导零移至时间栏 '{:0>4}'是指4位数右对齐格式，x达不到4位数时，用0补齐，例如0003
# '{:>4}'是指4位数右对齐格式，x达不到4位数时，左边空出相应的位数，例如  24.
# '{:0<8}'是指8位数左对齐，例如x=48,那么'{:0<8}'.format(x) =48000000
df_dropped.time =df_dropped.time.apply(lambda x: '{:0>4}'.format(x))
print(df_dropped.time.dtypes)       #对象类型
print(df_dropped.head())

#连接两列为一列数据
date_string =df_dropped['date'] + df_dropped.time
#转换为时间日期格式
date_times = pd.to_datetime(date_string,format ='%Y%m%d%H:%M') #unit='s', errors ='coerce'
print(date_times.head())

#将date_times设置为索引，新容器为df_clean
df_clean =df_dropped.set_index(date_times)
#删除不需要的列
df_clean =df_clean.drop(columns=['Date','time','useless'])
print(df_clean.head())


#筛选符合条件的行
#筛选出1号到5号的气温列
print(df_clean.loc['2010-01-01':'2010-01-05 9:00:00', 'Temperature'])

#把气温列转换为数值格式
df_clean['Temperature']=pd.to_numeric(df_clean.Temperature, errors='coerce')
#筛选出1号到5号的气温列
print(df_clean.loc['2010-01-01':'2010-01-05 9:00:00', 'Temperature'])

#describe statistik 描述统计量
print(df_clean.Temperature.describe())
print(df_clean.Temperature.median())
#某段数据的中位数,z.B.一月份的温度数据的中位数
print(df_clean.loc['2010-01','Temperature'].median())

#向下采样
#按天下采样，并且求每天的温度均值,保留2位小数
daily_mean =df_clean.resample('D').mean().round(2)
print(daily_mean.head())

#提取某列的值为数组
daily_temp =df_clean.Temperature.values
print(type(daily_temp))         #numpy.ndarray

#创建带有时间日期索引的时间序列
index =pd.date_range('2011-01-01',periods=8759, freq='H')
series1 =pd.Series(np.linspace(0,40,8759), index=index)
print(series1.head())

#下采样
series_daily =series1.resample('d').mean()
#.reset_index(drop=False)将原本的索引变成一列，现在的索引为顺序索引. .reset_index(drop=True)则是直接删除原本的索引列，现在的索引为顺序索引
series_temp =series_daily.reset_index(drop=True)
print(series_temp.head())

#数组与顺序索引的时间序列相减（注意数据长度要相同）
diff =daily_temp[0:365] -series_temp
#打印差额的平均值
print(diff.mean())

#筛选晴天数据
sunny= df_clean.loc[df_clean['sky_condition']=='CLR']
#筛选阴天数据
overcast=df_clean.loc[df_clean['sky_condition'].str.contains('OVC')]

# 重新取样晴天和阴天，按每日最高温度进行汇总
sunny_daily = sunny.resample('D').max()
overcast_daily = overcast.resample('D').max()

#打印平均值之间的差异
print(sunny_daily.mean()- overcast_daily.mean())

#每周平均温度和能见度
weekly_mean =df_clean[['visbility','dry_bulb_faren']].resample('w').mean()

# DataFrame.corr(method='pearson', min_periods=1, numeric_only=_NoDefault.no_default)
# method{‘pearson’, ‘kendall’, ‘spearman’}
# 计算列的成对相关性，不包括 NA/null 值。
# 周平均温度和能见度的相关性 Pearson correlation coefficient
print(weekly_mean.corr())

#画图
weekly_mean.plot(subplots=True)
plt.show()

sunny =df_clean['Temperature']>=58 #bool列 1/0
# 求和得到sunny每天为true的个数
sunny_hours =sunny.resample('d').sum()
print('sunny_hours:\n',sunny_hours)
#count()计数，对应每天有多少行数据
total_hours =sunny.resample('d').count()
print('total_hours:\n',total_hours )

# Divide sunny_hours by total_hours: sunny_fraction
sunny_fraction =sunny_hours/ total_hours

#画图
sunny_fraction.plot(kind='box',showmeans=True)
# plt.show()

#按月下采样，按最大值汇总
monthly_max= df_clean[['Temperature','date']].resample('m').max()
# print(monthly_max.head())

# 画图 直方图
# Generate a histogram with bins=8, alpha=0.5, subplots=True
# alpha 为颜色的透明度
monthly_max.plot(kind='hist', bins=8, alpha=0.5, subplots=True)
# plt.show()

# 高温的概率
# 提取九月最高温度
sep_max =df_clean.loc['2010-09','Temperature'].max()
print(sep_max)

#下采样,八月份每天的最高温
august =df_clean.loc['2010-08', 'Temperature'].resample('d').max()

#筛选出八月份温度高于sep_max的日子
august_high =august.loc[august > sep_max]

# 构建august_high的累积分布函数Cumulative distribution function
plt.figure()
august_high.plot(kind='hist', cumulative=True, bins=25)
plt.show()
