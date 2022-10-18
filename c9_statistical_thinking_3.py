#  通过优化进行参数估计
#  Parameter estimation by optimization

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(40)

mpg =pd.read_csv('./daten_file/mpg.csv', header=0)
hitter =mpg['mpg']

tau =np.mean(hitter)

#从参数为tau的指数分布中抽样
samples_ex =np.random.exponential(tau, 10000)

#画图 概率密度函数 PDF
#画法一：
plt.hist(samples_ex, bins=50, density=True, histtype='step')

#画法二：
plt.figure()
sns.histplot(data= samples_ex, bins=50, stat='density', element='step', fill=False)
plt.xlabel('Games between no-hitters')
plt.ylabel('PDF')
# plt.show()

# 数据是否跟随我们的故事？
# 画图 累积分布函数
plt.figure()
sns.histplot(data= samples_ex,bins=50, stat='density', element='step', fill=False, cumulative=True)
plt.margins(0.02)
plt.ylabel('CDF')

# 这个参数如何优化？
samples_half =np.random.exponential(tau/2, 10000)
samples_double =np.random.exponential(tau*2, size=10000)
#画图 累积分布函数
sns.histplot(data= samples_half,bins=50, stat='density', element='step', fill=False, cumulative=True)
sns.histplot(data= samples_double,bins=50, stat='density', element='step', fill=False, cumulative=True)
plt.legend(('EX=tau', 'EX=tau/2', 'EX=tau*2'), loc='best')
# plt.show()


# 识字/生育数据的 EDA
female =pd.read_csv('./daten_file/liter.csv',header=0)
# 画图  生育率（y 轴）与文盲率（x 轴）绘制为散点图
plt.figure()
plt.plot(female['female literacy'], female['fertility'], marker='.', linestyle='none')
plt.margins(0.02)
# plt.show()

#pearson相关系数
r_df =female[['female literacy','fertility']].corr(method='pearson')
r_coef =r_df.iloc[0,1].round(4) #保留四位小数
print(r_coef)



# 使用np.polyfit()进行线性回归：最小二乘多项式拟合Least squares polynomial fit
# Kleinste-Quadrate-Polynom-Anpassung
# z = numpy.polyfit(x, y, deg, rcond=None, full=False, w=None, cov=False) 返回多项式系数，阶数从高到低排列
# numpy.poly1d(c_or_r, r=False, variable=None) 返回一维多项式类。c_or_r: 多项式系数, 按照阶数从高到低排列
# p = np.poly1d(z) => 得到多项式 p= ax+b
# p(3) => 带入x=3, 3a+b
# 线性回归系数 a,b  f=ax+b   deg:degree 最高阶次数
a, b =np.polyfit(female['female literacy'], female['fertility'], deg=1)
print('slope:',a, '\nintercept: ',b)

#组成一维多项式 f= ax+b
f =np.poly1d([a,b])
print(f)
# 输出 x=5时， f的值
print(f(5))

# 分配x的值为 0和100
x= np.array([0,100])
# 以下写法等价：
y0 = a * x +b
y = f(x)
# print(y)

#画图
plt.plot(x,y)  #拟合线
# plt.show()



# 它是如何优化的？
# 获取回归参数的函数 np.polyfit() 会找到最佳斜率和截距
# 优化残差的平方和 optimizing the sum of the squares of the residuals

# 自定义斜率： 使用 np.linspace() 在 0 到 0.1 的范围内获得 200 个点
a_vals =np.linspace(0, 0.1, 200)

# empty_like() 函数返回一个与给定数组（在本例中为 a_vals）具有相同形状和类型的新数组
# 初始化残差平方和 RSS
rss =np.empty_like(a_vals)

# 计算不同斜率 对应的 残差平方和的值
# i指下标， a对应值
for i,a in enumerate(a_vals):
    rss[i] =np.sum((female['fertility'] - a*female['female literacy'] -b)**2 )

#画图  x =斜率 对应 y= 残差平方和
plt.figure()
plt.plot(a_vals, rss, '-')
plt.xlabel('slope (children per woman / percent illiterate)')
plt.ylabel('sum of square of residuals')
# plt.show()



# 线性回归
temp =pd.read_csv('./daten_file/weather_data.csv')
x1 = temp.Temperature
y1 = temp.DewPoint

#画图
plt.figure()
plt.plot(x1, y1, marker='.', ls= 'none', ms= 2)

#最小二乘 拟合
coef = np.polyfit(x1, y1, deg= 1)
f1 =np.poly1d(coef)

x_theo =np.array([40, 90])
y_theo =f1(x_theo)

#画拟合线
plt.plot(x_theo, y_theo)
# plt.show()


# 四个数据集 的线性回归斜率和截距
x_zusammen =[x1, mpg['mpg'], mpg.cyl, x1 ]
y_zusammen =[y1, mpg.weight, mpg.mpg, y1]

i=0
for x, y in zip(x_zusammen, y_zusammen):
    i +=1
    a, b =np.polyfit(x, y ,deg=1)
    print('斜率：',a, '截距：', b)
    print(i, ': f(x)=', np.poly1d([a,b]))

