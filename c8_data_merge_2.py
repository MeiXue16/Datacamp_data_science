# 连接数据

import pandas as pd

# DataFrame.append(other, ignore_index=False, verify_integrity=False, sort=False)
# 连接数据 默认纵向 要列名一致 => 构成一个更长的数据框

# 空列表中循环追加数据则不会构成一个数据框
units =[]
file_name =['jan', 'feb', 'mar']

for file in file_name:
    # '%s'%file 带入变量
    data ='%s_top.csv'%file
    df =pd.read_csv(data, index_col= 'Date',parse_dates= True)

    #空列表中循环追加数据： [ [...],[...], [...] ]
    units.append(df)
#纵向连接数据， keys: 最外层行索引，也就是被连接的数据框名。 names : 行索引标签名
quarter1 =pd.concat(units, ignore_index=False, keys= file_name, names=['month', 'Date'])


# 分割多索引dataframe

# medals 行索引： level = 0：['bronze', 'silver', 'gold'], level=1: 国家
# 按最外层行索引排序
medals_sorted =pd.DataFrame(medals).sort_index(level = 0)

# 打印德国铜牌数据
print(medals_sorted.loc[ ('bronze', 'Germany') ])

# 打印内层索引数据
print(medals_sorted.loc[['silver']])

# 打印英国获得的金银牌的所有数据
idx =pd.IndexSlice
print(medals_sorted.loc[ idx['silver':'gold','United Kingdom'], :])
# 等价于
print(medals_sorted.loc[ (slice('silver', 'gold'), 'United Kingdom') ])



# 横向串联以获得多索引列
#横向拼接数据 axis=1， keys: 最外层列索引，也就是被连接的数据框名
febr =pd.concat([df1, df2, df3], keys =['hardware','software','service'],axis=1)

#切片数据
idx =pd.IndexSlice
slice_2 =febr.loc['2015-2-2':'2015-2-8', idx[:, 'company']]



#用字典连接数据

#创建元组列表
month_list =[('january', jan), ('february',feb), ('march', mar)]
# 创建空字典
month_dict ={}

for month, data in month_list:
    #求不同公司的销售额
    month_dict[month] =data.groupby('company').sum()

# 连接数据 行索引 level 0: 月份， level 1: 公司
sales =pd.concat(month_dict)

#切片数据 Mediacore公司的所有数据
idx =pd.IndexSlice
print(sales.loc[ idx[:, 'Mediacore'], :])



# 下采样， 求百分比， 连接数据 inner join
#按年下采样，取每年最后一个值，求与前10年相比的百分比变化，去除空行
china_annual =china.resample('A').last().pct_change(periods=10).dropna()

us_annual =us.resample('A').last().pct_change(periods=10).dropna()

#横向连接数据， 只连接行索引相同的数据
gdp =pd.concat([china_annual,us_annual], join='inner', axis=1)



# 类似 inner join, 只能连接两张表： merge
# DataFrame.merge(right, how='inner', on=None, left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=True, indicator=False, validate=None

# on： 连接两张表的key列，
# 当两张表的key列名称不同时用：left_on, right_on
merge_by_city =pd.merge(revenue, managers, on ='city')

# how: left,right,inner,outer,cross
merge2 =pd.merge(revenue,managers, how='inner', left_on='city', right_on='branch' )

#多列组合为key
merge3 =pd.merge(revenue, manager, how='left', on =['branch_id','city', 'state'])


# 使用可选的填充/插值对有序数据执行合并, 可选择执行分组合并, 默认outer
# pandas.merge_ordered(left, right, on=None, left_on=None, right_on=None,
# left_by=None, right_by=None, fill_method=None, suffixes=('_x', '_y'), how='outer')
# left_by: 按组列对左 DataFrame 进行分组，并与右 DataFrame 逐个合并。
# suffixes: 指示要分别添加到 左右重叠列名的后缀
merge4 =pd.merge_ordered(austin, houston, on='date',suffixes=['_aus','_hus'],fill_method='ffill')



# merge_asof按关键距离执行合并。此函数可用于对齐不同的日期时间频率，而无需先重新采样
# 这类似于左连接，匹配最近的键而不是相等的键。
# 两个 DataFrame 都必须按 key 排序。

# pandas.merge_asof(left, right, on=None, left_on=None, right_on=None,
# left_index=False, right_index=False, by=None, left_by=None, right_by=None, suffixes=('_x', '_y'),
# tolerance=None, allow_exact_matches=True, direction='backward')

# left_index, right_index: bool值，按索引连接数据。有这个就不用on了
# by : 在执行合并操作之前匹配的列
# tolerance： int or Timedelta, 在此范围内选择asof公差；必须与合并索引兼容
# allow_exact_matchesbool, default True 则允许匹配相同的“on”值
# direction: ‘backward’ (default)匹配之前的, ‘forward’匹配之后的, or ‘nearest’匹配最近的

merge5 =pd.merge_asof(auto, oil, left_on='yr', right_on='Date',allow_exact_matches=True,
                      direction='forward', by='state', tolerance=pd.Timedelta('10s'))

# DataFrame.resample(rule, axis=0,on=None)
# on: 使用列而不是索引进行重采样。列必须类似于日期时间
weekly =merge5.resample('w',on='Date')[['mpg', 'price']].mean()

# DataFrame.corr(method='pearson', min_periods=1, numeric_only=_NoDefault.no_default)
#计算列的成对相关性， weekly有两列， 因此 w_corr是 2*2的矩阵
w_corr =weekly.corr()



