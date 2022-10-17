# 图形化探索性数据分析(EDA) Graphical exploratory data analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# from statsmodels.distributions.empirical_distribution import ECDF

#导入数据
mpg =pd.read_csv('./daten_file/mpg.csv',header =0)

#选择某列
length =mpg['mpg']

#画直方图
_ =plt.hist(length, bins=20, rwidth=0.8)
plt.xlabel('petal length (cm)')
plt.ylabel('count')

# plt.show()


# 计算数据点的数量
n_data =len(length)
n_data2 = length.count()
print(n_data ==n_data2)  #True

# 分组的数量(bins)是数据点数量的平方根
n_bins =int(np.sqrt(n_data))

# 画图
plt.figure()
_ =plt.hist(length, bins=n_bins, rwidth=0.8)

_ =plt.xlabel('petal length (cm)')
_ =plt.ylabel('Count')

# plt.show()


# 绘制ECDF图
# 经验累积分布函数
# empirical Cumulative Distribution Function
# 这里没有用到这个函数：ECDF(x, side='right')  right => [a, b) 返回跃阶函数（x 会按从小到大排序， y为累积分布率）

# 定义ecdf函数
def ecdf(data):
    # 計算数据長度
    n = len(data)
    # 排序
    x = np.sort(data)
    # 等分每個数据的間距
    y = np.arange(1, n + 1) / n
    return x, y

# 获取经验分布函数的x,y
x_vers, y_vers= ecdf(length)

#画图
plt.figure()
plt.plot(x_vers, y_vers, marker='.', linestyle='none', markersize=2)

#设置边缘
plt.margins(0.02)
plt.xlabel('length')
plt.ylabel('ECDF')
# plt.show()


# 比较经验分布函数
x_set, y_set= ecdf(mpg['size'])
x_vir, y_vir= ecdf(mpg['accel'])

#画图
plt.figure()
# linestyle/ ls , linewidth /lw,  marker, markersize / ms, color / c, alpha=0.8 透明度
plt.plot(x_vers,y_vers, marker='.', linestyle='none', alpha=0.5)
plt.plot(x_set,y_set, marker='o',linestyle='dashed')
plt.plot(x_vir,y_vir,marker='+',linestyle='-')
plt.margins(0.02)
plt.legend(('setosa', 'versicolor', 'virginica'),loc='lower right')
# plt.show()


# 定量探索性数据分析 Quantitative exploratory data analysis

#均值
mean_length =round(np.mean(length),2)
mean_length2=length.mean().round(2)
print(mean_length == mean_length2)      #True
print('length of versicolor: ', mean_length)


# 用sns 画箱形图 Box-and-wisker plot
plt.figure()
sns.boxplot(x='origin', y='mpg', data=mpg)

plt.xlabel('region')
plt.ylabel('length')
# plt.show()


#计算length的百分位数 [2.5, 25,50, 75] =>百分之2.5
percent =np.percentile(length, [2.5, 25,50, 75])
print(percent)
# 计算length的 分位数, 与上面的结果等价
quantile =np.quantile(length, [0.025, 0.25, 0.5, 0.75] )
quantile2=length.quantile([0.025, 0.25, 0.5, 0.75])
print(quantile2 == quantile)  #bool 列表 True


#计算方差

#方法一：按公式算 DX= E (X-EX)^2 =E(x^2)- (EX)^2
diff =length -length.mean()
variance1 = (diff**2).mean()

#方法二：函数var
variance2 =length.var()
variance3 =np.var(length)           #variance1 和variance3结果相同，尽量用np.var()
print(variance1, variance2,variance3)


#标准差
deviation1 =np.sqrt(variance3)
deviation2 =np.std(length)
print(deviation1 ==deviation2)      #true


#散点图
plt.figure()
plt.plot(length, mpg.cyl, marker='.', linestyle=None, ms=3 )
plt.margins(0.02)

plt.xlabel('petal length (cm)')
plt.ylabel('petal width (cm)')

# plt.show()


#计算协方差矩阵
covariance_matrix =np.cov(length, mpg.cyl)
print(covariance_matrix)

# 提取length与 mpg.cyl 之间的协方差
print(covariance_matrix[0,1])




#计算pearson 相关系数
#方法一：
def pearson_r(x,y):
    #求相关系数矩阵
    corr_mat =np.corrcoef(x,y)
    #返回 x 与 y 的相关系数
    return corr_mat[0,1]
r =pearson_r(length, mpg.cyl)
print(r)

#方法二：
r_df =mpg[['mpg','cyl']].corr( method='pearson')
r_p=  r_df.iloc[0, 1]
print(r_p )








