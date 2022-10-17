# 概率性思考——离散变量
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Generating random numbers using the np.random module
#使用np.random模块生成随机数

# Seed the random number generator
#给随机数发生器播种
np.random.seed(42)

#初始化随机数
# np.empty创建一个指定形状（shape）、数据类型（dtype）且未初始化的数组 （随机大小的值）
# np.empty(shape, dtype = float, order = 'C') 'F'
# np.empty([3,2], dtype =int)
random_numbers =np.empty(100000)

# np.zeros(shape, dtype = float, order = 'C')创建指定大小的数组，数组元素以 0 来填充
# np.ones(shape, dtype = float, order = 'C')创建指定形状的数组，数组元素以 1 来填充

# 通过在range(100000)上循环产生随机数
for i in range(100000):
    # np.random.random() 返回半开区间 [0.0, 1.0) 内的随机浮点数
    random_numbers[i] =np.random.random()

# np.random.rand(3,2) 返回[0.0, 1.0) 内的 3*2 的矩阵

#画图
plt.hist(random_numbers)
# plt.show()


# np.random 模块和 Bernoulli trials伯努利试验
# 做 n 次bernoulli实验成功的次数 的分布 => 二项分布
def bernoulli_trials(n, p):
    n_success =0
    for i in range(n):
        random_number =np.random.random()
        if random_number < p:
            n_success +=1
    return n_success

print(bernoulli_trials(1000,0.2))


# How many defaults might we expect?

np.random.seed(43)

#初始化长度为1000的随机数
n_defaults =np.empty(1000)

#分配值 100笔贷款中的违约数
for i in range(1000):
    n_defaults[i] =bernoulli_trials(100,0.05)


#画概率图
plt.figure()
plt.hist(n_defaults, density=True) # 面积为1，normed=True 已经被弃用了

# probability: or proportion: normalize such that bar heights sum to 1 标准化，使条形高度总和为 1
# density: normalize such that the total area of the histogram equals 1 归一化，使得直方图的总面积等于 1
# 用sns画概率图
plt.figure()
sns.histplot(data=n_defaults, stat='probability')
plt.xlabel('number of defaults out of 100 loans')
plt.ylabel('probability')
# plt.show()


# 银行会倒闭吗？
# 定义ecdf函数
def ecdf(data):
    # 計算数据長度
    n = len(data)
    # 排序
    x = np.sort(data)
    # 等分每個数据的間距
    y = np.arange(1, n + 1) / n
    return x, y

x1, y1 =ecdf(n_defaults)

#画图 方法一：
plt.figure()
plt.plot(x1, y1, marker='.', ls ='none', ms =2)
plt.margins(0.02)
plt.xlabel('defaults')
plt.ylabel('ECDF')
# plt.show()

#画图 方法二：(不好看)
plt.figure()
plt.hist(n_defaults, cumulative=True, histtype='step', density=True)
# plt.show()

#银行赔钱 大于或等于 10次 的概率
n_lose_money =np.sum(n_defaults >= 10) #true =>1, false=>0, 累加， 这里不能用count
print(n_lose_money/len(n_defaults))


# 直接从二项分布中抽样 np.random.binomial(n, p, size=None)
np.random.seed(44)
# 抽取 10,000 个样本
n_defaults2 =np.random.binomial(n=100, p=0.05, size=10000)

#累积分布函数
x2, y2 =ecdf(n_defaults2)
#画图
plt.figure()
plt.plot(x2, y2, marker='.', ms=3, ls='none')
plt.margins(0.02)
plt.xlabel('defaults')
plt.ylabel('ECDF')
# plt.show()


# 绘制二项 PMF 概率质量函数（probability mass function)
# 以下两种画法等价（分配了hist 的 bins的宽度=1）
bins1 =np.sqrt(len(n_defaults2))
bins2 =np.arange(0, max(n_defaults2) +1.5, 1) -0.5
plt.figure()
# 离散概率密度函数，总高=1, hist宽度为 1 时，总面积=1
# density 是指总面积=1
plt.hist(n_defaults2, bins= bins2, density= True)

plt.figure()
sns.histplot(n_defaults2, bins=bins2, stat='probability')
plt.margins(0.02)
# plt.show()


# 二项分布和泊松分布之间的关系 np.random.poisson(lam=1.0, size=None) lam= np =EX =DX
# 泊松分布是罕见事件的二项分布的极限。die Poisson-Verteilung ist ein Grenzwert der Binomialverteilung für seltene Ereignisse.
np.random.seed(45)
# 从泊松分布中抽取10,000个样本
samples_poisson =np.random.poisson(10, size=10000)

#打印样本均值和方差
print(np.mean(samples_poisson), np.var(samples_poisson))

#考虑二项分布的参数 n, p
n =[20,100, 1000]
p= [0.5, 0.1, 0.01]

for i in range(3):
    # 从二项分布中抽取10,000个样本
    samples_binomial= np.random.binomial(n[i], p[i], size=10000)
    # 输出均值和方差（n 越大 结果与poisson分布越接近）
    print('n= ', n[i], 'binomial:\n',
          np.mean(samples_binomial),
          np.var(samples_binomial))


# 2015 年异常吗？
np.random.seed(46)
# 从泊松分布中抽出10,000个样本
n_nohitters =np.random.poisson(251/115, size=10000)

# >=7的概率
n_large =np.sum(n_nohitters >= 7)
p_large =n_large/ len(n_nohitters)
print(p_large)



#连续函数

#正态分布概率密度函数 Normal PDF

# 从正态分布中抽出10000个样本  μ =20， std= σ =1/ 2/ 3
samples_std1 =np.random.normal(loc= 20, scale= 1, size=10000)
samples_std3 =np.random.normal(20, 3, size=10000)
samples_std10= np.random.normal(20, 10, size=10000)

#画图
plt.figure()
# histtype ='step' 生成默认未填充的线图
plt.hist(samples_std1, bins=100, density=True, histtype='step')
plt.hist(samples_std3, bins=100,density=True, histtype='step')
plt.hist(samples_std10, bins=100, density=True, histtype='step')
plt.legend(('std=1', 'std=3', 'std=10'), loc= 'best')
# 获取或设置当前坐标区的 y 限制 ylim(bottom, top)
plt.ylim(-0.01, 0.42)
# plt.show()

# 画法二：
samples =pd.DataFrame({'std1':samples_std1, 'std3':samples_std3, 'std10':samples_std10})
samples.plot(kind='hist', histtype='step', density=True, bins=100)
plt.ylim(-0.01, 0.42)
# plt.show()

#画法三：
plt.figure()
sns.histplot(data=samples, x='std1', stat='density', bins=100, element='step', fill= False)
# plt.show()



# 正态累计分布 Normal CDF
#画图
x3, y3 =ecdf(samples_std3)
# 画法一：
plt.figure()
plt.plot(x3, y3, marker='.', ls='none', ms =3)
# 设置自动缩放边距
plt.margins(0.02)
#画法二：(不够好，最后总是有一道竖线)
plt.figure()
plt.hist(samples_std3, histtype='step', bins=100, range=(5,40), density=True, cumulative=True)
#画法三：
plt.figure()
sns.histplot(data=samples_std3, bins=100, stat='density', element='step', fill=False, cumulative=True)
# plt.show()



# 贝尔蒙特赌注结果是否呈正态分布？
bel= pd.read_csv('./daten_file/mpg.csv',header= 0)
belmont =bel.loc[ :149, 'displ']
#设置series的索引
belmont.index =pd.date_range('1870-01-01', periods=150, freq='A')

# 查找异常值：最大最小值 以及 所在的行
max_idx =belmont.loc[belmont ==np.max(belmont)]
min_idx =belmont.loc[belmont ==belmont.min()]
print(max_idx, min_idx)

#按索引 删除最大最小值
belmont_no_ouliers =belmont.drop(index =['1957-12-31', '1888-12-31','1930-12-31'])

print(belmont_no_ouliers.info())

#求均值， 标准差
mu= np.mean(belmont_no_ouliers)
sigma= np.std(belmont_no_ouliers)

#设置正态分布10000个样本
np.random.seed(48)
samples_belmont =np.random.normal(mu, sigma, size=10000)

#画理论分布函数 & 实际分布函数
plt.figure()
#画法一：
sns.histplot(data =samples_belmont, cumulative= True, stat='density', bins=100,element='step', fill=False)
sns.histplot(data= belmont_no_ouliers, cumulative=True, stat='density', bins=100, element='step', fill =False)
plt.legend(('Theorie', 'Praxis'), loc='upper right')
plt.ylabel('CDF')
plt.margins(0.02)
plt.ylim(-0.01, 1.1)
# plt.show()
# 画法二：
plt.figure()
x4, y4 =ecdf(belmont_no_ouliers)
x_theo, y_theo =ecdf(samples_belmont)
plt.plot(x_theo,y_theo)
plt.plot(x4, y4)
plt.ylabel('CDF')
# plt.show()


# 一匹马匹配或击败秘书处记录的机会有多大？
np.random.seed(50)
sample_horse =np.random.normal(mu, sigma, size=10000)
# 计算样本<= 144的概率
prob =np.sum(sample_horse<=144) /len(sample_horse)
print('Probability of besting Secretariat:',prob)



# 如果你有故事，你可以模拟它！
# 泊松分布表示的是事件发生的次数，“次数”这个是离散变量，所以泊松分布是离散随机变量的分布；
# 指数分布是两件事情发生的平均间隔时间，“时间”是连续变量，所以指数分布是一种连续随机变量的分布。
# 指数分布 p(x) = λe^(-λx)        E(X)= β =1/λ
# random.exponential(scale=1.0, size=None) scale = 1/λ =EX

# 该函数返回两个事件的等待时间之和
def successive_poisson(tau1, tau2, size=1):
    # 从第一个指数分布中抽出样本
    t1 = np.random.exponential(tau1, size=size)
    t2 = np.random.exponential(tau2, size=size)
    return t1+t2


waiting_times =successive_poisson(764, 715, size=10000)
#画图 概率分布
plt.figure()
plt.hist(waiting_times, bins=100,histtype='step', density=True)
plt.xlabel('total waiting time (games)')
plt.ylabel('PDF')

#画法二：
plt.figure()
sns.histplot(data= waiting_times, bins=100, stat='probability', element='step', fill=False)
plt.show()













