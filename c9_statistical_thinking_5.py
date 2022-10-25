# 假设检验

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# numpy.concatenate((a1, a2, ...), axis=0, out=None, dtype=None, casting="same_kind")
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])
print(np.concatenate((a, b), axis=0)) #竖向连接
print(np.concatenate((a, b.T), axis=1)) #横向连接
print(np.concatenate((a,b), axis=None)) #展平 [1,2,3,4,5,6]

np.random.seed(45)

# np.random.permutation(x) 如果x是整数，则随机排列np.arange(x)。如果x是一个数组，则制作一个副本并随机打乱元素。
# 返回一个重新排列的数组（并且保持原始数组不变）。
print(np.random.permutation(10))

print(np.random.permutation([1, 4, 9, 12, 15]))

# np.random.shuffle(x)  Shuffle 意味着就地改变元素的排列。即在数组本身中
arr =np.array([1,2,3,4])
np.random.shuffle(arr)
print(arr)      #[1 3 2 4]



# 生成一个 排列组合样本 permutation sample

# permutation采样是模拟两个变量具有相同概率分布的假设的好方法
def permutation_sample(data1, data2):
    """Generate a permutation sample from two data sets."""

    # 纵向连接两个数据集
    data =np.concatenate((data1, data2))

    #排列组合（打乱）数组
    permuted_data =np.random.permutation(data)

    #把打乱后的数组分割为两个
    per_sample_1 =permuted_data[ :len(data1)]
    per_sample_2 =permuted_data[len(data1): ]

    return per_sample_1, per_sample_2


#导入数据
rainfall =pd.read_csv('./daten_file/rainfall.csv')
rain_july =rainfall.loc[rainfall.mm == 7, 'rain' ]
rain_nov =rainfall.loc[rainfall.mm ==11, 'rain']


# 假设检验：7 月（旱月）和 11 月（雨月）的月降雨量是否相同

# 可视化排列样本
# Visualizing permutation sampling
for i in range(50):
    per_sample_1, per_sample_2 =permutation_sample(rain_july, rain_nov)
    #累积分布函数图
    sns.histplot(per_sample_1, bins=100, stat='density', cumulative=True, element='step', fill=False, alpha=0.02)
    sns.histplot(per_sample_2, bins=100, stat='density', cumulative=True, element='step', fill=False, alpha=0.02)

#可视化实际数据
sns.histplot(rain_july, bins=100, stat='density', cumulative=True, element='step', fill=False)
sns.histplot(rain_nov, bins=100, stat='density', cumulative=True, element='step', fill=False)

plt.margins(0.02)
plt.xlabel('monthly rainfall (mm)')
plt.ylabel('ECDF')
# plt.show()



# 什么是 p 值？
# 是p-值“小”（小于给定的显着性水平；通常 < 0.05），表示观察到的数据与原假设充分不一致，可以拒绝原假设拒绝原假设。
# Der p-Wert ist definiert als die Wahrscheinlichkeit – unter der Bedingung, dass die Nullhypothese in Wirklichkeit gilt – den beobachteten Wert der Prüfgröße oder einen in Richtung der Alternative „extremeren“ Wert zu erhalten.
# 考虑观察到的检验统计量 t 来自未知分布 T
# p= P(|T| >= |t| | H0)

# Generating permutation replicates# 生成排列组合复制
def perm_reps(data1, data2, func ,size=1):
    perm_replicates =np.empty(size)
    for i in range(size):
        per_1, per_2 =permutation_sample(data1, data2)
        perm_replicates[i] =func(per_1,per_2 )
    return  perm_replicates


# 假设检验之前的 EDA
frog =pd.read_csv('./daten_file/frog.csv', comment='#', sep=',')
# 制作蜂群图
plt.figure()
sns.swarmplot(x= 'ID', y='impact force (mN)', data=frog)

plt.xlabel('frog')
plt.ylabel('impact force (N)')
# plt.show()



# 青蛙数据的排列检验 Permutation test on frog data
# 青蛙 A 的平均打击力为 0.71 牛顿 (N)，而青蛙 B 的平均打击力为 0.42 N，相差 0.29 N。青蛙的打击力可能相同，而观察到的差异是偶然的。
# 零假设 H0：成年青蛙 与 幼年青蛙 冲击力相同
#       H1: 实际差异 >= 实验中的平均冲击力的差异

# 我们使用均值差异的检验统计量的 permutation检验来检验这一假设
force_a =frog.loc[(frog.ID =='I') | (frog.ID=='II'), 'impact force (mN)']
force_b =frog.loc[(frog.ID =='III') | (frog.ID=='IV'), 'impact force (mN)']

def diff_of_means(data1, data2):
    diff =np.mean(data1) -np.mean(data2)
    return diff

# 计算实验中的平均冲击力的差异  Compute difference of mean impact force from experiment
empirical_diff_means =diff_of_means(force_a, force_b)

#10000个 permutation复制样本
perm_replicates =perm_reps(force_a, force_b, diff_of_means, size=10000)

#计算p值
p =np.sum(perm_replicates >= empirical_diff_means) /len(perm_replicates)

print('p-value=', p)  # p=0 <0.05, 拒绝原假设




# 单样本自举Bootstrap 假设检验
# 你想看看蛙 B 和蛙 C 是否有相似的冲击力。不幸的是，您没有 Frog C 的冲击力可用，但您知道它们的平均值为 0.55 N。因为您没有原始数据，
# 所以您无法进行permutation检验，并且您无法评估来自的力的假设Frog B 和 Frog C 来自同一个分布。因此，您将检验另一个限制较少的假设： bootstrap 假设检验，您将采用平均值作为我们的检验统计量。

# H0: Frog B 的平均打击力 = Frog C 的平均打击力 (Frog C数据未知)
# H1: Frog B 的平均打击力 >= Frog C 的平均打击力

# Frog C 的均值为 0.55 N, 模拟出Frog C数据
force_c =force_b -np.mean(force_b) +0.55

# Take bootstrap replicates 自举复制force_c
def bs_reps(data, func, size=1):
    bs_r =np.empty(size)
    for i in range(size):
        bs_r[i] = func(np.random.choice(data, size= len(data)))
    return bs_r

# 得到1000个force_c的平均冲击力的样本
bs_replicates =bs_reps(force_c, np.mean, 1000)

p_2= np.sum(bs_replicates <= np.mean(force_b))/ len(bs_replicates)

print('p = ', p_2)  #p=1 >0.05, 接受原假设




# 双样本 自举同分布检验 two sample bootstrap test for identical distributions
# H0：青蛙 A 和青蛙 B 具有相同分布的冲击力
# H1： DIFF>= diff (diff = mean(a)-mean(b) )

# 实验观察到的均值差异
emp_diff_means =diff_of_means(force_a, force_b)

# 纵向连接force_a 和 force_b
force_concat =np.concatenate((force_a, force_b), axis=0)

# 初始化 复制样本 (均值差)
bs_rep =np.empty(10000)

for i in range(10000):
    # 自举样本
    bs =np.random.choice(force_concat, size=len(force_concat))
    # 计算复制样本 (均值差)
    bs_rep[i] =diff_of_means(bs[: len(force_a)], bs[len(force_a): ])

#计算p值
p_3= np.sum(bs_rep >= emp_diff_means) /len(bs_rep)
print('p = ', p_3)      # p =  0.0001 < 0.05, 拒绝原假设



# two-sample hypothesis test for difference of means.
# 均值差的双样本假设检验可以通过: permutation test(更准确)/ bootstrap test 完成
# 单样本假设检验只能通过：bootstrap test 完成


# 如果 H0:青蛙A和青蛙B具有相同的平均冲击力，但不一定具有相同的分布。
# 这也是不可能用permutation检验的, 为了进行双样本自举测试，我们将两个阵列的平均数移至相同，因为我们正在模拟假设它们的平均数实际上是相等的。
# 然后，我们从移位后的阵列中抽取引导样本，并计算出平均值的差异。这就构成了一个引导复制，我们产生了许多这样的复制。
# p值是指均值差异大于或等于所观察到的差异的复制的比例。


# a 和 b 类青蛙的均值
mean =np.mean(force_concat)

# 转换样本值（使得force_a 和 force_b 均值相等）
force_a_new =force_a -np.mean(force_a) + mean
force_b_new =force_b -np.mean(force_b) +mean

# 自举复制样本
bs_a =bs_reps(force_a_new, np.mean, 10000)
bs_b =bs_reps(force_b_new, np.mean, 10000)

# 自举复制的均值差样本
bs_diff =bs_a -bs_b

#计算p值
p = np.sum(bs_diff >= mean)/len(bs_diff)
print('p-value= ', p)       #p= 0.0 <0.05,拒绝原假设













