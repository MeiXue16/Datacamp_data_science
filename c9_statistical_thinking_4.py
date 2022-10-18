# 自助法 Bootstrap Method
# 是一种从给定训练集中有放回的均匀抽样，也就是说，每当选中一个样本，它等可能地被再次选中并被再次添加到训练集中。
# Bootstrapping kann als Monte-Carlo Methode verstanden werden, da es wiederholt zufällige Stichproben einer Verteilung zieht
# 当样本来自能以正态分布来描述的总体，其抽样分布为正态分布；但当样本来自的总体无法以正态分布来描述，则以渐进分析法、自助法等来分析。

# 采用随机可置换抽样（random sampling with replacement）。对于小数据集，自助法效果很好。
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Bootstrap confidence intervals 置信区间

rainfall =pd.read_csv('./daten_file/rainfall.csv',sep=',')
print(rainfall.columns)
rain =rainfall['rain']
print(rain.info())
# Bootstrap样本可视化

# 从给定的一维数组生成随机样本 random.choice(a, size=None, replace=True, p=None)
# np.random.choice(5, size= 3) 从np.range(5)中(0~4)生成一个大小为3的均匀随机样本 <=> np.random.randint(0,5,3)
# np.random.choice(5, size=3, p=[0.1, 0, 0.3, 0.6,0])从np.range(5)中生成一个大小为3的非均匀的随机样本
# np.random.choice(5, size=10, replace= False)从np.range(5)中生成一个大小为10的均匀随机样本，不放回

# Generate bootstrap sample 生成5组自举样本
for i in range(5):
    bs_sample =np.random.choice(rain, size=len(rain))

    #画图 样本累积分布函数
    sns.histplot(data= bs_sample, stat='density', cumulative=True, element='step',fill=False, alpha=0.2)

#画图 实际累积分布函数

sns.histplot(data= rain, stat='density',cumulative=True,  element='step', fill=False)
plt.xlabel('yearly rainfall (mm)')
plt.ylabel('ECDF')

# plt.show()



# 生成许多自举复制

#定义函数 返回对一组bootstrap样本使用func
def bs_reps_1d(data, func):
    return func(np.random.choice(data, size=len(data)))

#返回 列表， 其中有size个 bs_reps_1d（）函数
def draw_bs_reps(data, func, size=1):
    bs_replicates= np.empty(size)
    for i in range(size):
        bs_replicates[i] =bs_reps_1d(data, func)
    return bs_replicates


# (统计量是样本均值，则称为均值的标准误)standard deviation of this distribution, called the standard error of the mean, or SEM

# 如果已知总体的标准差(σ)，那么抽取无限多份大小为 n 的样本，每个样本各有一个平均值，所有 这个大小的样本之平均值 的标准差为 sem = σ/√n standard deviation of sample mean
#
# 通常σ为未知，用取得样本的标准差 (s) 来估计sem:  sem = np.std(data) / np.sqrt(len(data)) = s/√n standard error of sample mean

# 理论上可以证明，在不太严格的条件下，均值的值总是呈正态分布的

#bootstrap 的 mean样本 和 SEM

#返回10000个年平均降雨量的样本
bs_reps =draw_bs_reps(rain, np.mean, size=10000)
#计算bs_reps的std (样本均值 的标准差)
bs_std =np.std(bs_reps)
print('standard deviation of bootstrap replicates:',bs_std)

# 已知总体的标准差(σ), 计算SEM （均值 的标准误差）
sem =np.std(rain)/ np.sqrt(len(rain))
print('SEM:',sem)

#画图 年均降雨量  近似正态分布
plt.figure()
plt.hist(bs_reps, bins=50, density=True, histtype='step')
plt.xlabel('mean annual rainfall (mm)')
plt.ylabel('PDF')
# plt.show()



# 其他统计量的Bootstrap replicates ,例如size个样本方差作为统计量
bs_reps2 =draw_bs_reps(rain, np.var, size=10000)

# 把方差以平方厘米为单位计算
bs_reps2 =bs_reps2 /100

#画图
plt.figure()
plt.hist(bs_reps2, bins=50, density=True, histtype='step')
plt.xlabel('variance of annual rainfall (sq. cm)')
plt.ylabel('PDF')
# plt.show()


# no_hitter的置信区间
# print(rainfall.info())
no_hitter =pd.to_numeric(rainfall['mm'], errors='coerce')

# no_hittter的均值的bootstrap replicates
bs_reps3 =draw_bs_reps(no_hitter, np.mean, size=10000)

# 95% 的置信区间
conf_int =np.percentile(bs_reps3, [2.5, 97.5])
print('95% confidence interval :', conf_int)

# 画图
plt.figure()
plt.hist(bs_reps3, bins=50, density=True, histtype='step')
plt.xlabel(r'$\tau$ (mean of games)')
plt.ylabel('PDF')
# plt.show()



# A function to do pairs bootstrap

# 对线性回归进行成对自举分析 Perform pairs bootstrap for linear regression
def draw_ba_pairs_linreg(x,y, size=1):
    # 设置索引数组，以便从中取样
    inds =np.arange(len(x))

    #初始化副本
    bs_slope_reps =np.empty(size)
    bs_intercept_reps=np.empty(size)

    #生成副本
    for i in range(size):
        bs_inds =np.random.choice(inds, size=len(inds))
        bs_x, bs_y =x[bs_inds], y[bs_inds]
        bs_slope_reps[i], bs_intercept_reps[i] =np.polyfit(bs_x,bs_y, deg=1)
    return bs_slope_reps, bs_intercept_reps

#导入数据
female =pd.read_csv('./daten_file/liter.csv')
x =female['female literacy']
y =female['fertility']

# 使用成对自举法生成斜率和截距的重复数据
slope_list, intercept_list =draw_ba_pairs_linreg(x, y, size=1000)

# 斜率的95%置信区间
ci_slope =np.percentile(slope_list, [0.025, 0.975])
print(ci_slope)

#画图 斜率
plt.figure()
plt.hist(slope_list, bins=50, density=True, histtype='step')
plt.xlabel('slope')
plt.ylabel('PDF')
# plt.show()



# 绘制自举回归图
plt.figure()
x1=np.array([0,100])
print(slope_list[0])
for i in range(100):
    y1 =slope_list[i] * x1 + intercept_list[i]
    f= np.poly1d([slope_list[i], intercept_list[i] ])
    y2 =f(x1)
    plt.plot(x1, y2, lw=0.5, alpha=0.2, color='red')

#实际数据图
plt.plot(x, y, marker='.', ls='none')
plt.xlabel('literacy')
plt.ylabel('fertility')
plt.margins(0.02)
plt.show()
