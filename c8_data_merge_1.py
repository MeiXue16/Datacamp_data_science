# 准备数据  Preparing data

#循环读取多个文件中的DataFrame
import numpy as np
import pandas as pd

#创建文件名列表
file =['./daten_file/daten1.csv', './daten_file/daten2.csv', './daten_file/daten3.csv']

#创建dataframe列表
dataframe =[]
for i in file:
    dataframe.append(pd.read_csv(i))

#打印dataframe列表 中的第一个列表的前五行
print(dataframe[0].head())


# 组合来自多个数据文件的DataFrames
#导入数据
sales =pd.read_csv('./daten_file/sales.csv')

#复制数据框 sales
medals =sales.copy()

#更改列名
medals.columns =['date', 'gold', 'salt', 'salat']

#添加新列 (与来自其他数据框的列 行数不同时，会自动修改为 medals的行数)
medals['silver'] =dataframe[0].loc[:, 'Vorname']
medals['bronze'] =dataframe[2].iloc[:,3]
print(medals)


# 使用索引和列对 DataFrame 进行排序

# 设置索引为某列
weather =pd.read_csv('./daten_file/weather_data.csv')
weather =weather.set_index(pd.to_datetime(weather['Date'], format='%Y%m%d %H:%M'))
print(weather.head())
print(weather.info())

# 按索引排序, 降序
weather2 =weather.sort_index(ascending= False)

# 按某列排序,默认升序
weather2 =weather.sort_values('Temperature')



# 重新设置数据框架的索引

#重新设置索引, 要求与原本索引 长度相同
weather2 =weather.set_index(np.arange(8759))

# reindex 可以用于交换索引行/列顺序（值也会相应改变），扩展数据框，因此reindex 要与原本的索引行/列 相同，或扩展本的索引行/列
# 创建列表
year =pd.date_range('2009-12-31 22:00', periods=9000, freq='H')

# 空值用‘hello’填充
weather3 =weather.reindex(year, fill_value='hello')

# 用后面的值填充前面的空值
weather4 =weather.reindex(year, method= 'bfill')
print(weather4.head())

#打印数据框形状
print( weather4.shape)

#删除空行
weather4 =weather4.dropna()
print(weather4.shape)


# 算术公式中的广播
# 广播一词是指 numpy 在算术运算期间如何处理具有不同维度的数组，这会导致某些约束，较小的数组在较大的数组中广播，以便它们具有兼容的形状。
# 广播允许对大小不同的张量执行算术运算。在满足某些约束时自动将“较小”张量广播到“较大”张量的大小

# 提取某些列组成新的dataframe
temp_f =weather.loc[:, ['Temperature','DewPoint','Pressure']]
# 更改列名
temp_f.columns =['TempF','DewF','PressF']

# 广播
temp_c =(temp_f- 32)* 5/9
# 更改列名
temp_c.columns =temp_c.columns.str.replace('F', 'C')
print(temp_c.head())



# 计算某列增长百分比
#导入数据，设置索引，解析索引为日期格式
wea =pd.read_csv('./daten_file/weather_data.csv',index_col='Date', parse_dates= True)
# print(wea.head())

# 取6月1号后的所有数据
post6 =wea.loc['2010-06-01':]
print(post6.tail())

# 按天下采样，取每天最后一个值
daily =post6.resample('d').last()

# 当前元素和先前元素之间的百分比变化。默认情况下计算前一行的百分比变化
# DataFrame.pct_change(periods=1, fill_method='pad', limit=None, freq=None, **kwargs)
percentage_growth =daily.pct_change()*100
percentage_growth.columns =['Temp_growth', 'Dev_growth','Press_growth']

print(percentage_growth.head())

#横向连接2个数据框
zusammen =pd.concat([daily,percentage_growth], ignore_index=False, sort= True, axis=1 )
print(zusammen.head())

#更改列顺序
zusammen =zusammen.reindex(['Temperature', 'Temp_growth', 'DewPoint', 'Dev_growth', 'Pressure', 'Press_growth'],axis=1)
print(zusammen.head())



# dataframe之间的乘法（二元运算符mul）
# df.multiply(other_df, axis='columns', level=None, fill_value=None)

sale =pd.read_csv('./daten_file/sales.csv')
sale2 =sale.iloc[:, 1: ]
print(sale2)

# df与一列数据相乘：（axis =0）行与行相乘时 行索引要一致， 因此将原本的日期索引删除，替换为顺序索引
zusammen2= zusammen.reset_index()
# 相乘时 长度要一致，因此截取前6行（包含索引5对应的行）
zusammen2 =zusammen2.loc[:5, :]
print(zusammen2)

#df与一列数据 相乘 （与行相乘）
mul =sale2.mul(zusammen2['Temperature'],axis=0)
print(mul)

#df与一行数据 相乘 （与列相乘）
mul2 =sale2.mul([1,2,3], axis=1)
print(mul2)