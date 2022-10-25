# 假设检验示例
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 排除“出席”和“弃权”票，153 名众议院民主党人和 136 名共和党人投了赞成票。然而，91 名民主党人和 35 名共和党人投了反对票。
# 党派关系对投票有影响吗？（民主党赞成率：62%， 共和党赞成率：79%）
# H0: 议员所在政党对其投票没有影响
# H1: 有影响，民主党赞成率 < = 62%

# 你将使用民主党人投赞成票的比例作为你的测试统计量，并评估观察到民主党人投赞成票的比例至少与观察到的比例153/244一样小的概率。
# 要做到这一点，需要对众议院选民的党派标签进行修改，然后任意将其分为 "民主党人 "和 "共和党人"，并计算出民主党人投票赞成的比例。

# #1964年对《民权法案》的投票

# 构造各方投票的布尔数组
dems =np.array([1]* 153 + [0] * 91)
reps =np.array([True]* 136 +[False] *35)
# print(dems)

# 返回投赞成票的民主党人所占比例 returns the fraction of Democrats that voted yay
def frac_yay_dems(dems, data):
    frac =np.sum(dems)/len(dems)
    return frac

#permutation样本
def perm_sample(data1, data2):
    concate_sample =np.concatenate((data1, data2))
    permuted = np.random.permutation(concate_sample)
    perm1 =permuted[ :len(data1)]
    perm2 =permuted[len(data2): ]
    return perm1, perm2

#permutation 自举复制
def perm_reps(data1, data2, func, size=1):
    replicates =np.empty(size)
    for i in range(size):
        per1, per2 =perm_sample(data1,data2)
        replicates[i] =func(per1, per2)
    return replicates


# 获得自举复制样本 （混合后排列组合，任意划分出的民主党人投票赞成率）
perm_replicates =perm_reps(dems, reps, frac_yay_dems, 10000)

#计算p值
p1 =np.sum(perm_replicates <= 153/244)/ len(perm_replicates)
print('p =', p1)        #p = 0.0004 < 0.05 ,拒绝原假设



# 网站上的时间模拟
# A/B测试为一种随机测试，将两个不同的东西（即A和B）进行假设比较
#  A/B测试可以用来测试某一个变量两个不同版本的差异，一般是让A和B只有该变量不同，
#  再测试其他人对于A和B的反应差异，再判断A和B的方式何者较佳

# 1920 年，美国职业棒球大联盟实施了重要的规则变更，结束了所谓的死球时代。重要的是，投手不再被允许在球上吐口水或擦伤球，这是一项非常有利于投手的活动。
# 在这个问题中，您将执行 A/B 测试以确定这些规则更改是否会导致更慢的无命中率（即，无安打者之间的平均时间更长）使用平均无安打者时间的差异作为您的测试统计数据。

# H0 ： 1920年前后 no_hitter的 平均间隔时间 不变
# H1 : |T| > = |empirical_diff_of_means|

no_hitter =pd.read_csv('./daten_file/hitter.csv', index_col=0, parse_dates=True)
# print(no_hitter.info())
# 按时间索引划分数据
nht_dead =no_hitter.loc[ : '1920-12-31', 'game_number']
nht_live =no_hitter.loc['1921-1-1': , 'game_number' ]
# print(nht_live.head())

def diff_of_means(data1, data2):
    # 若不改为绝对值（np.abs()）的话， 需要注意empirical_diff的值是否为大于0的值。若小于0， 那么 H1要改为perm_replicates2 <= empirical_diff
    diff = np.mean(data1) -np.mean(data2)
    return diff

#计算1920年前后数据的均值差
empirical_diff =diff_of_means(nht_dead, nht_live)
print(empirical_diff)  # -108979

#制作permutation复制样本 （10000个均值差样本）
perm_replicates2 =perm_reps(nht_dead, nht_live, diff_of_means, 10000)

#计算p值, 左侧检验
p2 =np.sum(perm_replicates2 <= empirical_diff)/ len(perm_replicates2)
print('p =',p2)     #p = 0.0 <0.05 拒绝原假设




# 模拟有关相关性的零假设

female =pd.read_csv('./daten_file/liter.csv')
literacy =female['female literacy']
fertility =female.fertility

# 在 162 个国家的数据集中观察到女性文盲和生育率之间的相关性可能只是偶然；一个特定国家的生育率实际上可能与其文盲完全无关

# H0： 文盲和生育率不相关
# H1: T >= t右侧检验   T<=t左侧检验  |T| >= |t|对称双侧检验

# pearson相关假设检验

# 计算观察到的相关性
r_obs = np.corrcoef(literacy, fertility)[0,1]
print(r_obs.round(3))   # -0.804

#初始化permutation复制 (相关性)
perm_replicates3 =np.empty(10000)

#制作permutation复制
for i in range(10000):
    # 排列文盲值，但保持生育率值不变
    literacy_permuted= np.random.permutation(literacy)
    perm_replicates3[i] = np.corrcoef(literacy_permuted, fertility)[0,1]

#计算p值， 左侧检验
p3 =np.sum(perm_replicates3 <= r_obs)/len(perm_replicates3)
print('p =', p3)        # p = 0.0 <0.05 拒绝原假设




# 研究新烟碱类杀虫剂 对蜜蜂繁殖 的影响

# 研究杀虫剂 如何影响 每半毫升精液中活精子的数量
#导入数据
bees =pd.read_csv('./daten_file/bees.csv', comment='#', sep=',')
# 未经处理的蜜蜂 的活精子
control_sperm =bees.loc[bees.Treatment=='Control', 'Sperm Volume per 500 ul']
# 用杀虫剂处理的蜜蜂 的活精子
treated_sperm =bees.loc[bees.Treatment=='Pesticide', 'Sperm Volume per 500 ul']

# EDA：绘制未经处理 的蜜蜂 和 用杀虫剂处理的蜜蜂 的活精子计数的 ECDF。
sns.histplot(data= control_sperm, bins=100, stat='density', cumulative=True, element='step', fill= False)
sns.histplot(data= treated_sperm, bins=100, stat='density', cumulative=True, element='step', fill= False)
plt.margins(0.02)
plt.xlabel('millions of alive sperm per 0.5 mL')
plt.ylabel('ECDF')
plt.legend(('control','treated'), loc= 'lower right')
# plt.show()


# 蜜蜂精子数量的自举假设检验 Bootstrap

# H0: 未经处理 和 用杀虫剂处理的蜜蜂 的活精子 的平均数量相等
# H1： T>= t (t =未经处理 和 用杀虫剂处理的蜜蜂 的活精子 的平均数量差异)

# 计算 t (观察到的平均差异)
empi_diff_means =np.mean(control_sperm) -np.mean(treated_sperm)
print(empi_diff_means.round(3))      # 429891.571



# 双样本 自举同分布检验
# 纵向连接两个样本， 求连接后的样本均值
sperm =np.concatenate((control_sperm, treated_sperm),axis=0)
sperm_mean =np.mean(sperm)

# 自举样本( 直接连接两个样本后自举， 就不用考虑a和b样本的均值差。

#  若从force_a 中自举a, force_b中自举b, 则需要对force_a 和 force_b的均值统一化)
# 生成移位的数据集，使移位后的数据集具有相同的平均值
control_shift = control_sperm -np.mean(control_sperm) +sperm_mean
treated_shift = treated_sperm -np.mean(treated_sperm) + sperm_mean

# 自举复制样本函数
def bs_reps(data, func, size=1):
    bs_replicates=np.empty(size)
    for i in range(size):
        bs_replicates[i] =func(np.random.choice(data, size= len(data)))
    return bs_replicates

# 生成自举复制样本（均值差）
# 以下两种写法等价：
# 方法1：从a中自举a, b中自举b
bs_rep_sperm = bs_reps(control_shift, np.mean, 10000) - bs_reps(treated_shift, np.mean, 10000)
# 方法2：混合后自举
bs_rep_sperm2 =np.empty(10000)
for i in range(10000):
    bs_sample = np.random.choice(sperm, size=len(sperm))
    bs_rep_sperm2[i] = diff_of_means( bs_sample[: len(control_sperm)], bs_sample[len(control_sperm): ])

# 计算p值
p4 =np.sum(bs_rep_sperm >= empi_diff_means)/ len(bs_rep_sperm)
print('p =',p4)         #p = 0.003 <0.05,拒绝原假设














