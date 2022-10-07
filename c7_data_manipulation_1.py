import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#提取和转换数据
#index_col =0,第一列作为索引列
pennsy =pd.read_csv('./daten_file/pennsy.csv',header=0, index_col='county')

#用两种方法提取dataframe的第一列和第二列数据, 返回bool列（true）
print(pennsy.loc[:,['state', 'total']]== pennsy.iloc[:, [0,1]])

#用几列数据创建新的dataframe
results =pennsy[ ['winner', 'total', 'voters'] ]
results2 =pennsy.loc[:, ['winner', 'total', 'voters'] ]
results3 =pennsy.iloc[:, [4,1,5]]
print(type(results))        #<class 'pandas.core.frame.DataFrame'>
print(type(results2))       #<class 'pandas.core.frame.DataFrame'>
print(results == results2, results2== results3) #bool列 true

# 切片行标签, 从'Perry' 到 'Potter'（包含Potter）,等价于
#    pennsy.loc['Perry':'Potter':, ]
# 或 pennsy.loc['Perry':'Potter']
p_counties =pennsy.loc['Perry':'Potter', :]
print(p_counties)

# 切片行标签,按照相反的顺序将行标签切片，也就是'Potter'到'Perry'
p_counties_rev=pennsy.loc['Potter':'Perry':-1, :]
print(type(p_counties_rev))     #<class 'pandas.core.frame.DataFrame'>

#分割列(包含'Obama')
left_columns =pennsy.loc[:, :'Obama']
left_columns2 =pennsy.iloc[:, :3]
print(left_columns.head())
#分割列（包含'winner'）
middle_columns =pennsy.loc[:,'Obama':'winner']
print(middle_columns.head())
#分割列， 从'Romney'到最后一列
right_columns =pennsy.loc[:,'Romney': ]

#用列表来选择dataframe
rows = ['Philadelphia', 'Centre', 'Fulton']
cols = ['winner', 'Obama', 'Romney']
# 创建新的DataFrame,3*3
three_counties =pennsy.loc[rows, cols]
print(three_counties.head())

# 阈值化数据Thresholding data
#筛选 列turnout > 70的行数据
high_turnout = pennsy.turnout > 70
high_turnout_df =pennsy.loc[high_turnout]
print(high_turnout_df.head())

# 筛选 margin <1的行数据
too_close =pennsy.margin <1
# 对于margin <1对应的'winner'列的值为 np.nan
pennsy.loc[too_close, 'winner'] =np.nan
print(pennsy.info())

#导入数据
titanic =pd.read_csv('./daten_file/daten1.csv',header=0, names=['a','age','cabin','b','c'])
#创建新df
df =titanic[['age', 'cabin']]
print(df.shape)     #(59, 2)
#删除df中任意的缺失值所在的行（默认axis =0）
print(df.dropna(how ='any').shape) #(54, 2)
#删除df中一整行都为NaN的行
print(df.dropna(how='all').shape) #(59, 2)
#保留 至少有50个非空值 的列
print(df.dropna(thresh=50, axis=1).info())


# 数据自定义转换
# 使用 apply() 转换列
def to_celsius(F):
    return 5/9*(F- 32)

#导入数据
weather =pd.read_csv('./daten_file/weather_data.csv', header=0)
#选取前两列作为新的数据框
weatherDataFrame =weather.iloc[:, :2]
print(weatherDataFrame.head())
#对df运用to_celsius函数(两行效果等价)
df_celsius =weatherDataFrame.apply(to_celsius)
df_celsius2 =weather[['Temperature','DewPoint']].apply(to_celsius)
# 断言两者等价
assert (df_celsius==df_celsius2).all().all()
#给新的df分配新的列名
df_celsius.columns =['Mean TemperatureC', 'Mean Dew PointC']



# map()函数将给定函数应用于可迭代对象（列表、元组等）的每个项目并返回一个迭代器。
# map(funktion, object)
# # pandas.Series.map() 方法用于 根据Python dictionary look-up  转换值.
# 根据输入映射或函数映射 Series 的值。用于将 Series 中的每个值替换为另一个值
# s.map({'cat': 'kitten', 'dog': 'puppy'}) 将序列s中的cat映射为kitten
# s.map('I am a {}'.format) 将序列s中的cat映射为 I am a cat
# 为了避免将函数应用于缺失值（并将它们保留为 NaN）na_action='ignore'

# Series.map(arg, na_action='ignore')
red_vs_blue={ 'Obama':'blue','Romney':'red' }
# 使用字典将 'winner' 列中的值 'Obama' 和 'Romney' 映射到值 'blue' 和 'red'，并将输出分配给新列 'color'
pennsy['color']= pennsy['winner'].map(red_vs_blue)
print(pennsy.head())

# 当性能至关重要时，您应该避免使用 .apply() 和 .map()，因为这些构造对存储在 pandas Series 或 DataFrame 中的数据执行 Python for 循环。

# vectorized functions 向量化函数
from scipy import stats
# 计算样本中每个值相对于样本均值和标准差的 zscore(standardisierte Zufallsvariable)
# Z= (X- μ)/ σ, 如果Z为负数，则表示观察值低于平均值
turnout_zscore =stats.zscore(pennsy['turnout'])
print(type(turnout_zscore))     #<class 'pandas.core.series.Series'>
print(turnout_zscore.head())
#将标准化随机变量列分配给pennsy的新列
pennsy['turnout_zscore'] = turnout_zscore
print(pennsy.head())


# 更改 DataFrame 的索引
#把pennsy的索引列修改为全部大写单词
new_idx =[x.upper() for x in pennsy.index]
pennsy.index =new_idx

# 更改索引名称标签
pennsy.index.name ='COUNTY'

# 添加列名标签
pennsy.columns.name= 'products'
print(pennsy.head())

# 单独构建DataFrame和index，然后放在一起(长度要一致)
months =pd.date_range('2010-01', periods=67, freq='m')
pennsy.index =months

pennsy['county'] =months
print(pennsy.head())



# 使用 MultiIndex 提取数据
# 设置多重索引
pennsy =pennsy.set_index(['county', 'color'])
#访问MultiIndex 的最外层（与单级索引的情况一样）
print(pennsy.loc[['2010-01-31','2010-05-31']])
print(pennsy['2010-01-31':'2010-05-31'])

# 设置和排序 MultiIndex，
# 使用 MultiIndex，您应该始终确保索引已排序
pennsy =pennsy.sort_index()
print(pennsy.head())

# 多重索引 MultiIndex 的多个级别

# 索引1：'2010-01-31'索引2：'red'的行
jan_red =pennsy.loc[[ ('2010-01-31', 'red')]]
print(jan_red)

#'2010-2-28'和'2010-03-31'的数据
jan_n =pennsy.loc[( ['2010-2-28','2010-03-31'], slice(None)), :]
#等价于
jan_n2 =pennsy.loc[ ['2010-2-28','2010-03-31']]
assert (jan_n == jan_n2).all().all()

#从'2010-01-31'到'2012-01-31'期间，color为blue 的行数据
f_blue =pennsy.loc[ (slice('2010-01-31','2012-01-31'), 'blue'),: ]
print(f_blue)

#所有的color为 blue的行数据
blue =pennsy.loc[ (slice(None), 'blue'), :]
print(blue)