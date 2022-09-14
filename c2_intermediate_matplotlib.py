#package matplotlib
import matplotlib.pyplot as plt
import numpy as np
x1 = np.linspace(-8,8,100)  #创建等差数列 从-8到 8，生成 100个点
x2 = np.arange(0,10,0.1)   #创建等差数列 从0 到 99.9， 间隔为 0.1
y1 = np.sin(x1)/x1
y2 = 2 * np.sin(x2)

plt.figure()                    #新建画布
plt.plot(x1,y1, label='y1')     #折线图，图标为 y1
plt.scatter(x2,y2, label='y2', c='r')  #散点图
plt.title('title')  #生成标题
plt.xlabel('x')     #x轴标签
plt.ylabel('y')
plt.legend()        #生成图例
plt.xscale('log')   #把x轴设置为log对数轴

plt.figure()        #新建画布
plt.hist(y2, bins=5)     #直方图，无间隙，5个条形，y轴为某个值出现的次数，即频率分布
plt.clf()           #清空画布，5个条形的直方图不会被显示出来

plt.hist(y2, bins=15)

plt.figure()        #新建画布
x3 = np.linspace(0,10,100)
y3 = np.sin(x3)/3
svalue = x3/5
plt.scatter(x3,y3, s=svalue, c='g', alpha= 0.8 ) # s= 粗细程度, alpha=0~1透明度

tick_val = [0.1,1,10]
tick_lab = ['0,1','1,0','10,0']
plt.xticks(tick_val,tick_lab)  # 调整X轴上的刻度线，并给他们命名
plt.text(3, 0.1, 'India')       #在（3，0.1）坐标点上添加文本‘India’
plt.grid(True)                  #生成坐标格



#subfigure
fig, ax =plt.subplots(nrows=1, ncols=2)     #一行两列的子图
ax[0].plot(x1,y1,label='figure 1')
ax[1].scatter(x2,y2,label='figure 2')
ax[0].legend(loc='upper left')  #生成第一张图的图例
ax[0].set_title('title')
ax[0].set_xlabel('x1')
ax[0].set_ylabel('y1')


fig, ax =plt.subplots(nrows=2, ncols=2)     #2行2列的子图
ax[0,0].plot(x1,y1,label='figure 1')
ax[0,1].scatter(x2,y2,label='figure 2')
ax[0,0].legend(loc='upper left')  #生成第一张图的图例
ax[0,0].set_title('title')
ax[0,0].set_xlabel('x1')
ax[0,0].set_ylabel('y1')


plt.show()          #生成图像