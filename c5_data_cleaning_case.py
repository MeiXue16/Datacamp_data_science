import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#导入文件为dataframe
g1800s =pd.read_csv('./daten_file/gapminder.csv')

#画散点图，识别异常值
plt.figure()
plt.scatter(x=g1800s['1800'], y=g1800s['1899'] )
plt.xlabel('life expectancy in 1800')
plt.ylabel(' life expectancy in 1899')

#等价于上面的画图,不需要新建画布
g1800s.plot(kind='scatter', x='1800', y='1899')

plt.show()

#检查数据, 检查除了第一列，其他列的值是否都 >=0
def check_null_or_valid(row_data):
    #除了第一列以外，其他列包含null/ numeric
    #删除其他列的空值
    no_na = row_data.dropna()[1: ]
    #将其他列的值都转换为numeric
    numeric =pd.to_numeric(no_na)
    #判断值是否>=0，返回bool值
    return numeric>=0

#编写断言语句以确保 g1800s 数据帧的第一列（索引 0）是“预期寿命”
assert g1800s.columns[0] =='Life expectancy'

#断言 除了第一列，其他列的值都 >=0
assert g1800s.iloc[:, 1:].apply(check_null_or_valid, axis=1).all().all()

#断言 每个国家/地区在数据中仅出现一次(.value_counts()[0] 会返回分类计数频次最高的值)
assert g1800s['Life expectancy'].value_counts()[0] ==1


#导入文件
g1900s= pd.read_csv('./daten_file/gapminder.csv')
g2000s =pd.read_csv('./daten_file/gapminder.csv')

#纵向连接数据
gapminder =pd.concat([g1800s, g1900s, g2000s], ignore_index= True,sort= False,join= 'outer')

#打印连接数据的形状
print(gapminder.shape)

#打印前五行
print(gapminder.head())

#reshaping 重塑数据: melt 宽数据 => 长数据
#不变的列为'Life expectancy'， 其他的列都融化为一列variable,一列value
gapminder_melt =pd.melt(gapminder, id_vars = ['Life expectancy'])

#重命名列名
gapminder_melt.columns =['country', 'year', 'life_expectancy']


#检查数据类型
print(gapminder_melt.info())

#更改数据类型为int
gapminder_melt['year'] =pd.to_numeric(gapminder_melt['year'])

# 断言 country 是 object 类型，
assert gapminder_melt.country.dtype ==np.object
# 断言 year 是 int64 类型，
assert gapminder_melt.year.dtypes ==np.int64
# 断言 life_expectancy 是 float64 类型
assert gapminder_melt.life_expectancy ==np.float64

#检查特殊字符/无效字符 => 正则表达式 re
#检查国家的拼写
# 创建国家序列
countries =gapminder['country']

#删除重复项
countries =countries.drop_duplicates()

#pattern 正则表达式， 哪些字符属于国家/地区的假设
pattern ='^[A-Za-z\.\s]*$'

# bool值向量，判断countries列的值是否符合pattern
mask = countries.str.contains(pattern)

#取反
mask_inverse = ~mask

#显示无效的国家名 (筛选数据)
invalid_countries =countries.loc[mask_inverse]

#处理丢失数据
# 可以删除它们，这样做可能最终会丢弃有用的信息
# 或者使用缺失值所在的列或行的平均值填充它们（也称为插补）
# 如果您正在处理时间序列数据，则使用前向填充或反向填充，用该列中最近的已知值替换列中的缺失值 （pandas Foundations）

#断言国家和年份不包含任何缺失值
assert pd.notnull(gapminder.country).all()
assert pd.notnull(gapminder.year).all()

#删除'life_expectancy'缺失值的行， how和axis都是默认值
gapminder= gapminder.dropna(subset=['life_expectancy'],how='any',axis =0 )

#打印形状
print(gapminder.shape)


# 收尾工作
# 现在你有了一个干净整洁的数据集，你可以做一些可视化和聚合

#subplot 和subplots用法稍有不同
#建一张 2*1的画布，在第1个位置上画图
plt.subplot(2,1,1)
gapminder['life_expectancy'].plot(kind ='hist')

#这些年来平均预期寿命的变化
gapminder_agg= gapminder.groupby('year')['life_expectancy'].mean()

print(gapminder_agg.head())
print(gapminder_agg.tail())

#画图
plt.subplot(2,1,2)
gapminder_agg.plot()
plt.show()

#保存至csv文件中
gapminder.to_csv('gapminder.csv')
gapminder_agg.to_csv('gapminder_agg.csv')




