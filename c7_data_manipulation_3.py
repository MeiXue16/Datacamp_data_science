# 分组数据
import pandas as pd
import numpy as np
from scipy import stats

# DataFrame.groupby(by=None, axis=0, level=None, as_index=True, sort=True,
# group_keys=_NoDefault.no_default, squeeze=_NoDefault.no_default, observed=False, dropna=True)

# 使用 apply()时，用group_keys包含或排除组键。该group_keys参数默认为True
# df.groupby("Animal", group_keys=True).apply(lambda x: x)

titanic =pd.read_excel('./daten_file/titanic.xlsx')
print(titanic.head())
# 按“pclass”列分组
by_class =titanic.groupby('pclass')
# 按“pclass”列分组, 'survived'的个数
count_by_class =by_class['survived'].count()
print(count_by_class)

# 按多列分组
by_mult =titanic.groupby(['embarked', 'pclass'])
count_mult =by_mult['survived'].count()
print(count_mult)

# Grouping by another series 按另一个序列分组
life =pd.read_csv('life_fname.csv', index_col='country' )

regions =pd.read_csv('regions_fname.csv', index_col='country')

#按regions['region'] 分组 life
life_by_region =life.groupby(regions['region'])

# 分组后 2010列的 均值
print(life_by_region['2010'].mean())
#

# 计算多列的多个聚合
by_class =titanic.groupby(by ='pclass')     #等价于groupby('pclass')
agg =by_class[['age','fare']].agg([max, 'median'])
print(agg)
#多重列索引 用元组调用：'age'列的'max'列
print(agg.loc[:, ('age', 'max')])
print(agg.loc[:, ('fare', 'median')])


# 聚合索引级别/字段
#有 multiindex 多重行索引时，可用level指定分组级别。不要同时指定by和level。

#读取数据
titan = pd.read_excel('./daten_file/titanic.xlsx')
titan =titan.set_index(['pclass', 'sex', 'survived'])
#对索引排序
titan =titan.sort_index()
#根据'pclass', 'sex'分组
group_1 =titan.groupby(level =[0,1])

#定义函数
def spread(series):
    return series.max() -series.min()
#创建字典
aggdic ={'age':'mean', 'fare':spread, 'boat':'count'}

#使用字典聚合group_1
aggregated =group_1.agg(aggdic)
print(aggregated)

# 对索引的函数进行分组

sales =pd.read_csv('./daten_file/weather_data.csv', index_col='Date', parse_dates=True)
print(sales.head())
# Series.dt.strftime(*args, **kwargs) string format time
# strftime('%B %d, %Y, %r')  B => Month , r => 09:00:01 AM
# strftime使用指定的 date_format 转换为索引。 %a => 周一 ~ 周日
sales.index = sales.index.strftime('%a')
#索引排序，在这里没用，这里是按str的首字母排序的
sales =sales.sort_index()
by_day =sales.groupby(sales.index)

#聚合
units_sum =by_day.Temperature.sum()
print(units_sum)

# 使用 Z 分数检测异常值
# z分数对于查找异常值很有用：z 分数值 +/- 3 通常被认为是异常值
pennsy =pd.read_csv('./daten_file/pennsy.csv')
from scipy.stats import zscore
# 计算两列的zscore (groupby + transform/apply)
std_zscore =pennsy.groupby('state')[['total', 'Obama']].transform(zscore)
print(std_zscore)
# 构建一个布尔系列来识别异常值：
outlier =( np.abs(std_zscore['total']>3) ) | (std_zscore['Obama']<-3)
# 筛选出异常值行
p_outliers = pennsy.loc[outlier]
print(p_outliers)


# 按组 填充缺失数据（插补）
by_class2 = titanic.groupby(['sex', 'pclass'])
def impute(series):
    return series.fillna(series.median())
# transform 函数 1.只允许在同一时间在一个Series上进行一次转换，如果定义列‘a’ 减去列‘b’，  则会出现异常；
# 2.必须返回与 group相同的单个维度的序列（行）
# 3. 返回单个标量对象也可以使用，如 . transform(sum)

titanic.age =by_class2.age.transform(impute)
# print(titanic.info())
# titanic.to_excel('titan_age.xlsx')

# .apply 的其他转换
# 1. 不同于transform只允许在Series上进行一次转换， apply对整个DataFrame 作用
# 2.apply隐式地将group 上所有的列作为自定义函数

#按性别分组
titanic =titanic.dropna(subset=['sex'])
sex =titanic.groupby('sex')

# 定义函数， 求age的分布和zscore,并将结果输出到一个dataframe中
def disparty(data):
    s = data['age'].max() -data['age'].min()
    # z = stats.zscore(data['age'])
    z = (data['age'] -data['age'].mean())/ data['age'].std()
    dict ={'zscore(age)': z, 'spread(age)':s }
    # return dict
    return pd.DataFrame(dict)
#按性别 求age的分布和zscore
sex_df =sex.apply(disparty)
print(sex_df)


# 使用 .apply() 进行分组和过滤
# 计算“C”甲板上的平均存活率
def c_deck_survival(gr):
    c_passengers = gr['cabin'].str.startswith('C').fillna(False)
    return gr.loc[c_passengers, 'survived'].mean()
# 按性别分组
by_sex =titanic.groupby('sex')
# 应用c_deck_survival函数
c_surv_by_sex =by_sex.apply(c_deck_survival)
# 打印女性c甲板存活均值
print(c_surv_by_sex.loc[['female']])

# 使用 .filter() 进行分组和筛选
sales1 =pd.read_csv('./daten_file/sales-feb-2015.csv')
# 按公司分组
by_company =sales1.groupby('Company')
#打印分组后 'Units' 列的sum
print(by_company['Units'].sum())
#筛选出符合条件的行（分组后 'Units' 列的sum 大于35的数据）
print(by_company.filter(lambda x: x['Units'].sum() > 35))


# 使用 .map() 进行筛选和分组
under10 =(titanic['age']<10).map({True:'under 10', False:'over 10'})
# 按10岁上下分组，求存活平均数
mean_survived =titanic.groupby(under10)['survived'].mean()
print(mean_survived)

#按10岁上下和pclass分组，求存活均值
mean_survived2 =titanic.groupby([under10, 'pclass'])['survived'].mean()
print(mean_survived2)

