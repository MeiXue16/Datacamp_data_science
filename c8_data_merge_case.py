# 案例研究 - 夏季奥运会

import pandas as pd

# 导入数据，分隔符为tab
editions =pd.read_csv('./daten_file/Summer Olympic medals/Summer Olympic medalists 1896 to 2008 - EDITIONS.tsv', sep='\t')

# 提取需要的列
editions =editions[['Edition', 'Grand Total', 'City','Country']]

print(editions.head())

# 导入数据
ioc_codes=pd.read_csv('./daten_file/Summer Olympic medals/Summer Olympic medalists 1896 to 2008 - IOC COUNTRY CODES.csv')
# 提取需要的列
ioc_codes= ioc_codes[['Country','NOC']]

print(ioc_codes.tail())


medals_dict={}
for year in editions['Edition']:
    #文件地址
    # :d Decimal format
    file_path ='./daten_file/summer/summer_{:d}.csv'.format(year)
    #加载文件，并分配为字典key(year)对应的值
    medals_dict[year] =pd.read_csv(file_path)

    #覆盖为文件部分列
    medals_dict[year] =medals_dict[year][['Athlete', 'NOC','Medal']]

    # 新建一列，值为年份
    medals_dict[year]['Edition']= year

#纵向连接数据
medals =pd.concat(medals_dict, ignore_index=True)


#在数据透视表中按国家/年份计算奖牌数
medal_count =medals.pivot_table(index='Edition', columns='NOC', values='Athlete', aggfunc='count')


#计算每个奥运年份的奖牌比例
#设置索引为年份
totals =editions.set_index('Edition')

#提取一列出来
totals =totals['Grand Total']

# 用奖牌数除以总数 ,medal_count的第一行都除以totals[0], 第二行都除以totals[1]
fraction =medal_count.div(totals, axis=0)



#计算获得奖牌的百分比变化
# DataFrame.expanding(min_periods=1, center=None, axis=0, method='single')提供扩展窗口计算

#求累计均值
mean_frac =fraction.expanding().mean()

#求百分比变化 *100
frac_pct_change =fraction.pct_change()*100

#删除原有索引，使用顺序索引, 原本的索引变成第一列
frac_pct_change =frac_pct_change.reset_index()



#left join 合并数据
hosts =pd.merge(editions, ioc_codes, on= 'Country',how='left')
print(hosts.head())

# 提取相关列
hosts =hosts[['Edition','NOC']].set_index('Edition')

# 修复hosts的'NOC'值缺失问题
print(hosts.loc[hosts.NOC.isnull()])
hosts.loc[1972, 'NOC'] ='FRG'
hosts.loc[1980, 'NOC']= 'URS'
hosts.loc[1988, 'NOC']= 'KOR'

#删除原有索引，使用顺序索引, 原本的索引变成第一列
hosts =hosts.reset_index()
print(hosts)



# 宽数据 => 长数据
reshaped =pd.melt(frac_pct_change, id_vars='Edition', value_name='change')

print(reshaped.shape)

chn =reshaped.loc[reshaped.NOC =='CHN']


#合并数据
merged =pd.merge(reshaped, hosts, hoe='inner')

influence = merged.set_index('Edition').sort_index()

print(influence.head())


#画图
import matplotlib.pyplot as plt
change =influence['change']

ax =change.plot(kind='bar')

ax.set_ylabel('% Change of Host Country Medal Count')
ax.set_title('Is there a Host Country Advantage?')
ax.set_xticklabels(editions['City'])
plt.show()







