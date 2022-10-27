# case study
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 达尔文雀的喙部深度的EDA EDA of beak depths of Darwin's finches
# Create bee swarm plot 创建蜂群图
beak_1975 =pd.read_csv('./daten_file/beak_1975.csv')
beak_1975['date'] = pd.date_range('1975-01-01', periods=403, freq='d')

print(beak_1975.tail())

beak_2012 =pd.read_csv('./daten_file/beak_2002.csv')
beak_2012['date'] =pd.date_range('2012-01-01',periods=248,freq='D')
print(beak_2012.tail())

#连接两个数据集方法一：
beak_zusa =np.concatenate((beak_1975, beak_2012), axis=0)
print('beak_zusammen np.concatenate 第4列:', beak_zusa[:,3])

#连接两个数据集方法二：
#修改部分列名
beak_1975.rename(columns={'Beak length, mm':'blength', 'Beak depth, mm': 'bdepth'},inplace=True)
print(beak_1975.head())
#连接两个数据集
beak_zusammen =pd.concat([beak_1975,beak_2012], ignore_index=True, join='inner')

#按 date列 排序，升序
beak_zusammen=beak_zusammen.sort_values('date', ascending=True)

#新建一列:year (提取 时间日期的 年份)
beak_zusammen['year'] =beak_zusammen.date.dt.year

#画图 蜂群图
sns.swarmplot(data=beak_zusammen, x='year', y='bdepth')

plt.xlabel('year')
plt.ylabel('beak depth (mm)')
# plt.show()


#分别画出他们的 ECDF 累积分布函数
plt.figure()
sns.histplot(data=beak_1975,x ='bdepth', bins=100, stat='density', cumulative=True, element='step', fill=False )
sns.histplot(data=beak_2012,x='bdepth', bins=100, stat='density', cumulative=True, element='step', fill=False )

plt.legend(('1975','2012'), loc='best')
plt.xlabel('beak depth (mm)')
plt.ylabel('ECDF')
# plt.show()



#参数估计 Parameter estimates of beak depths
bd_1975 =pd.to_numeric(beak_1975['bdepth'])
bd_2012 =pd.to_numeric(beak_2012['bdepth'])

#计算实际的样本均值差
empi_mean_diff =np.mean(bd_2012)- np.mean(bd_1975)

#bootstrap 自举复制均值样本
def bs_reps(data, func, size=1):
    bs_replicates =np.empty(size)
    for i in range(size):
        bs_replicates[i]=func(np.random.choice(data, len(data)))
    return bs_replicates

bs_rep_1975 =bs_reps(bd_1975, np.mean, 10000)
bs_rep_2012 =bs_reps(bd_2012, np.mean, 10000)

#bootstrap replicates 自举复制均值差样本
bs_mean_diff = bs_rep_2012- bs_rep_1975

#95%的置信区间
conf_int_bd =np.percentile(bs_mean_diff, [2.5, 97.5])

print('95% confidence interval =',conf_int_bd)
print('difference of means =', empi_mean_diff)  #-0.223



# 假设检验
# H0：1975年 和 2012年 鸟喙的深度 没变化
# H1: T <= t (t= empi_mean_diff = -0.223  2012年的鸟喙的深度更短)

# 计算总样本均值
mean =np.mean(np.concatenate( (bd_1975, bd_2012) , axis=0 ) )

# 转换样本，使得两个样本的均值相同
bd_1975_shift =bd_1975 -np.mean(bd_1975) +mean
bd_2012_shift =bd_2012 -np.mean(bd_2012) +mean

# 自举复制均值样本
bs_rep_1975_shift =bs_reps(bd_1975_shift,np.mean, 10000)
bs_rep_2012_shift =bs_reps(bd_2012_shift, np.mean,10000)

# 自举复制 均值差样本
bs_diff =bs_rep_2012_shift -bs_rep_1975_shift

# 计算p值 （bs_diff <= -0.223）左侧检验
p =np.sum(bs_diff <= empi_mean_diff)/ len(bs_diff)

print('p =', p)     #p = 0.0001 <0.0001 拒绝原假设




# 喙的长度和深度的EDA  EDA of beak length and depth

plt.figure()
#散点图
# plt.plot(beak_1975['blength'], beak_1975.bdepth, marker='.', ls='none', color='blue', alpha=0.5)
# plt.plot(beak_2012.blength, beak_2012.bdepth, marker='.', ls='none', color='red',alpha=0.5)
sns.scatterplot(data=beak_1975, x='blength', y='bdepth', style='species', color='skyblue', label='1975')
sns.scatterplot(data=beak_2012, x='blength', y='bdepth', style='species', color='pink', label='2012')

plt.legend( loc='best')
plt.xlabel('beak length (mm)')
plt.ylabel('beak depth (mm)')
# plt.show()

# 从散点图明显看出 两种鸟有不同的趋势，fortis和 scandens各需要一条拟合回归线

# 1975年的两种鸟的拟合回归线
fortis_1975 =beak_1975.loc[beak_1975.species =='fortis']
scandens_1975 =beak_1975.loc[beak_1975.species =='scandens']

slope_fortis_1975, inter_fortis_1975 = np.polyfit(x= fortis_1975.blength, y= fortis_1975.bdepth, deg=1)
slope_scandens_1975, inter_scandens_1975= np.polyfit(x=scandens_1975.blength, y=scandens_1975.bdepth, deg=1)
print('fortis_bdepth1975= ', np.poly1d([slope_fortis_1975, inter_fortis_1975] ) ,
      '\nscandens_bdepth1975= ', np.poly1d( [slope_scandens_1975, inter_scandens_1975]))


# 2012年的两种鸟的拟合回归线
fortis_2012 =beak_2012.loc[beak_2012.species =='fortis']
scandens_2012 =beak_2012.loc[beak_2012.species =='scandens']

coe_fo_2012 = np.polyfit(x= fortis_2012.blength, y=fortis_2012.bdepth, deg=1)
coe_sa_2012 =np.polyfit(x=scandens_2012.blength, y= scandens_2012.bdepth,deg=1)

f_fortis_2012 = np.poly1d(coe_fo_2012)
f_scanden_2012 =np.poly1d(coe_sa_2012)
print('fortis_bdepth2012 = ', f_fortis_2012,
      '\nscandens_bdepth2012 = ', f_scanden_2012)


# 线性回归 + 成对自举 pairs bootstrap
# fortis 的拟合回归的自举复制

def bs_linreg(x, y ,size=1):
    inds =np.arange(len(x))
    slope , intercept =np.empty(size), np.empty(size)
    for i in range(size):
        bs_inds =np.random.choice(inds, size=len(inds))
        bs_x, bs_y = x[bs_inds], y[bs_inds]
        slope[i], intercept[i] =np.polyfit(bs_x, bs_y, deg=1)
    return slope,intercept

#提取数据
fortis =beak_zusammen.loc[beak_zusammen.species =='fortis']
#重置索引
fortis =fortis.reset_index()
# print(fortis.tail())

# fortis 的拟合回归的自举复制
slope_fortis_bs, inter_fortis_bs =bs_linreg(fortis.blength, fortis.bdepth, size=10000)

# fortis 斜率, 截距 的95%置信区间
confi_fortis_slope =np.percentile(slope_fortis_bs, [2.5, 97.5])
confi_fortis_inter =np.percentile(inter_fortis_bs, [2.5,97.5])

print('confidence intervall of fortis_slope= ', confi_fortis_slope,
      '\nconfidence intervall of fortis_intercepet= ', confi_fortis_inter)



#显示线性回归的结果

x =np.array([9,12])

for i in range(50):
    f = np.poly1d([slope_fortis_bs[i], inter_fortis_bs[i]])
    plt.plot(x, f(x), lw=0.5, alpha=0.2, color='skyblue')
# plt.show()




# 喙的长度与深度比
# 计算长度与深度的比率
ratio_1975 =beak_1975.blength /beak_1975.bdepth
ratio_2012 =beak_2012.blength /beak_2012.bdepth

#计算比率均值
mean_ratio_1975 =np.mean(ratio_1975)
mean_ratio_2012 =np.mean(ratio_2012)

# 自举复制 均值比率 样本
bs_ratio_1975 =bs_reps(ratio_1975, np.mean, 10000)
bs_ratio_2012 =bs_reps(ratio_2012, np.mean, 10000)

# 计算 均值比率 95%置信区间
confi_1975 =np.percentile(bs_ratio_1975, [2.5, 97.5])
confi_2012 =np.percentile(bs_ratio_2012, [2.5, 97.5])

print('1975: mean ratio= ', mean_ratio_1975,
      '\nconfidence intervall 1975 =', confi_1975,
      '\n2012: mean ratio= ', mean_ratio_2012,
      '\nconfidence intervall 2012 =', confi_2012)



# fortis遗传性的EDA
herit =pd.read_csv('./daten_file/heritability.csv')

bd_parent =(herit['Male BD'] +herit['Female BD'])/2

#散点图
plt.figure()
plt.plot(bd_parent, herit['Mid-offspr'], marker='.', ls='none', color='skyblue', alpha=0.5)

plt.xlabel('parental beak depth (mm)')
plt.ylabel('offspring beak depth (mm)')

# plt.show()


# 参数估计：pearson 相关系数
corr_empi =np.corrcoef(bd_parent, herit['Mid-offspr'])[0,1]

# pearson 相关系数+ 成对自举
def bs_corr(x, y, size=1):
    inds=np.arange(len(x))
    bs_reps =np.empty(size)
    for i in range(size):
        bs_indx =np.random.choice(inds, len(inds))
        bs_x, bs_y =x[bs_indx], y[bs_indx]
        bs_reps[i] = np.corrcoef(bs_x, bs_y)[0,1]
    return bs_reps

bs_r =bs_corr(bd_parent, herit['Mid-offspr'], 1000)

# 参数估计： 95%的置信区间
confi_r =np.percentile(bs_r, [2.5, 97.5])

print('empirical correlation=', corr_empi,
      '\nconfidence intervall =', confi_r)




# 测量遗传性 (相关系数)

# 协方差 = EXY- EXEY =E(X-EX)(Y-EY)
# 协方差表示的是两个变量的总体的误差
# 如果两个变量的变化趋势一致，也就是说如果其中一个大于自身的期望值，另外一个也大于自身的期望值，那么两个变量之间的协方差就是正值。
# 如果两个变量的变化趋势相反，即其中一个大于自身的期望值，另外一个却小于自身的期望值，那么两个变量之间的协方差就是负值。
# 如果X与Y是统计独立的，那么二者之间的协方差就是0，因为两个独立的随机变量满足E[XY]=E[X]E[Y]。
# 但是，反过来并不成立。即如果X与Y的协方差为0，二者并不一定是统计独立的。

# 协方差为0的两个随机变量称为是不相关的
# ρ =cov(x,y)/(sqrt(varx)* sqrt(vary))
def heritability(parents, offspring):
    covariance_matrix =np.cov(parents, offspring)
    # pearson 相关系数 ρ
    return covariance_matrix[0,1]/np.sqrt(covariance_matrix[0,0] *covariance_matrix[1,1])

# 计算遗传性
heritability_correlation =heritability(bd_parent, herit['Mid-offspr'])
print('Correlation coefficient calculated from the covariance matrix=', heritability_correlation)


#自举复制相关性样本
def bs_pairs(x, y, func, size=1):
    inds=np.arange(len(x))
    bs_reps =np.empty(size)
    for i in range(size):
        bs_indx =np.random.choice(inds, len(inds))
        bs_x, bs_y =x[bs_indx], y[bs_indx]
        bs_reps[i] = func(bs_x, bs_y)
    return bs_reps

bs_herit =bs_pairs(bd_parent,herit['Mid-offspr'], heritability, size=1000)

# 95%置信区间
conf_int_r = np.percentile(bs_herit,[2.5, 97.5])

print('confidence intervall=', conf_int_r)



# 在*G. scandens*中，喙的深度是否可以遗传？
# Is beak depth heritable at all in *G. scandens*?

# 利用permutation replicates更改 x: bd_parent, y保持不变， 再计算它们的相关性
# H0: 不一定可以遗传
# H1: T>= t (t = heritability_correlation样本相关性)

#初始化array of replicates
perm_array =np.empty(1000)

for i in range(1000):
    bd_parent_perm =np.random.permutation(bd_parent)
    perm_array[i] =heritability(bd_parent_perm, herit['Mid-offspr'])


# 计算 p值
p_herit =np.sum(perm_array >= heritability_correlation) / len(perm_array)
print('p-val = ', p_herit)
















