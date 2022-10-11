#案例研究

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#导入数据
medals =pd.read_csv('./daten_file/all_medalists.csv',header=0)

#按年份分组的，美国得奖的数据
usa_edition_grouped =medals.loc[ medals.NOC =='USA'].groupby('Edition')

#提取NOC列,几种写法等价
country_names =medals.loc[:, ['NOC']]
country_names2 =medals.loc[:, 'NOC']
country_names3 =medals.NOC
country_names4 =medals['NOC']

#对NOC列分类计数
medal_counts =country_names3.value_counts()

#打印前15名得奖国家
print(medal_counts.head(15))

# 透视表
# 此处values 可以等于 ‘Athlete’（运动员），'Sport'，'Edition'等等（除了index和columns指定的列）
# values：若没有聚合函数，则显示values对应的值; 若有aggfuc,则显示聚合后的values
counted =medals.pivot_table(index ='NOC', values='Edition', columns='Medal',aggfunc='count')

# 给透视表添加一列'totals'，横向计算每个国家的奖牌总和数
counted['totals'] =counted.sum(axis='columns')
# 按'totals'列排序透视表
counted= counted.sort_values('totals',ascending=False)
print(counted.head(15))

# 去重 .drop_duplicates()
# 取两列，两种取法等价
ev_gen =medals.loc[:, ['Event_gender', 'Gender']]
ev_gen2 =medals[['Event_gender', 'Gender']]

#去重，只留下独特的行
ev_gen_uniques =ev_gen.drop_duplicates()

print(ev_gen_uniques)


# 使用 .groupby() 查找可能的错误
# 按'Event_gender', 'Gender'分组后计数
medal_count_by_gender =medals.groupby(['Event_gender', 'Gender']).count()
print(medal_count_by_gender)


# 通过定位违规行来检查可疑记录
suspect =medals.loc[ (medals.Event_gender == 'W') & (medals.Gender == 'Men' )]
print(suspect)

# .nunique() to rank by distinct sports
# 使用 .nunique() 按不同的运动排名
# DataFrame.nunique(axis=0, dropna=True) 计算指定轴中不同元素的数量。
# 按国家分组
group_noc =medals.groupby('NOC')
# 每个国家不同运动的数量序列
Nsports =group_noc['Sport'].nunique()
# 对序列进行排序
Nsports =Nsports.sort_values(ascending=False)
print(Nsports.head(15))

# 汇总冷战期间美国和苏联获奖的不同运动项目的数量
during_cold_war = (medals.Edition >= 1952) & (medals.Edition<=1988)
is_usa_urs =(medals.NOC== 'USA') | (medals.NOC== 'URS')
cold_war_medals =medals.loc[during_cold_war & is_usa_urs ]

Nsports =cold_war_medals.groupby('NOC')['Sport'].nunique().sort_values(ascending=False)
print(Nsports)


# 计算美国与苏联冷战奥运奖牌
#透视表
medals_won_by_country =medals.pivot_table(index='Edition', columns ='NOC', values='Athlete', aggfunc='count')
# 1952年至1988年期间，美国和苏联各自赢得的奥运奖牌总数
cold_war_usa_usr_medals = medals_won_by_country.loc[1952:1988, ['USA', 'URS']]

# 1952年至1988年期间，美国和苏联各自赢得的奥运奖牌总数最多的国家序列。
# idxmax(axis=0, skipna=True, numeric_only=False)返回所请求轴上第一次出现的最大值的索引
most_medals =cold_war_usa_usr_medals.idxmax(axis= 'columns')
print(most_medals.head())

# 1952年至1988年期间，美国和苏联各自赢得的奥运奖牌总数比对方多的次数。
print(most_medals.value_counts())


# 按年份可视化美国奖牌计数
# 筛选美国的数据
usa =medals.loc[ medals.NOC=='USA' ]
# 按'Edition', 'Medal'分组，计数获奖数（可以对运动员，性别，运动等等计数，结果相同）
usa_medals_by_year =usa.groupby(['Edition', 'Medal'])['Athlete'].count()

print(usa_medals_by_year.head())

# 把行索引'Medal'转换为 列索引， 等价于level =-1, level = 1
usa_medals_by_year =usa_medals_by_year.unstack(level='Medal')

print(usa_medals_by_year.head())


# 画图，两种画法等价, x默认为行索引，y默认为每一列，列索引为每条折线的标签
# usa_medals_by_year.plot( y=['Bronze','Gold','Silver'] , kind ='line')
usa_medals_by_year.plot(title ='USA Medal Counts by Edition', ylabel='number of medals')
# plt.show()

# 面积图,两种画法等价
# usa_medals_by_year.plot(kind='area')
usa_medals_by_year.plot.area()
# plt.show()


# 有顺序（'Bronze', 'Silver', 'Gold'）的奖牌面积图
# 方法1：在处理数据时，重新定义'Medal'列 为一个有序的分类符号，再进行筛选透视
medals.Medal = pd.Categorical(values =medals.Medal, categories=['Bronze', 'Silver', 'Gold'], ordered=True)
# 筛选出美国的数据
usa2 =medals.loc[medals.NOC=='USA']
# 透视表
usa_group =usa2.pivot_table(index='Edition', columns ='Medal', values='Athlete',aggfunc='count')
print(usa_group.head())
usa_group.plot(kind='area')

#方法2：对筛选出的透视表的列名进行更改，排序，再替换，实现列的交换
# 修改列名
usa_medals_by_year.columns =[0,2,1]
#对列索引重新排序，默认升序
usa_medals_by_year= usa_medals_by_year.sort_index(axis=1)
# 修改列名
usa_medals_by_year.columns =['Bronze', 'Silver', 'Gold']
print(usa_medals_by_year.head())
usa_medals_by_year.plot(kind='area')
plt.show()

