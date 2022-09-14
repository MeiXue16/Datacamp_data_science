import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#df = pd.DataFrame(np.arange(0,16,1).reshape(4,4), index=list('abcd'), columns= list('ABCD'))
df=pd.DataFrame(np.arange(16).reshape(4,4),index=list('abcd'),columns=list('ABCD'))
print(df.loc['a'])
print(df.iloc[0]) #提取a行

print(df.loc[['a','d']])
print(df.iloc[[0,3]]) #提取多行

print(df.loc[:,['A']])
print(df.iloc[:,[0]]) #提取某列

print(df.loc[:,['A','C']]) #提取多列

print(df.loc[['a'],['D']])
print(df.iloc[0,3]) #提取值

print(df.loc[['a','c'], ['A','B']])

print(df.loc['a':'c', 'A':'B'])

print(df.loc[:,:])
print(df)

print(df.loc[(df['A']==0)&(df['B']==1)])
print(df[df['A']==0])
print(df[(df['A']==0) & (df['B']==1)])
# print(df[['A']])
# print(df['A'])

df_average= np.mean(df['A'])
print(df_average)

print(np.std(df))

print(np.var(df))

print(df.head(2))
print(df.tail(3))

df.drop(columns='A', inplace=True) #删除某列
print(df)
fig, ax= plt.subplots()
# x1 =np.linspace(-8,8,100)
# y1= np.sin(2*x)

x1 =df['B']
#x1 =df['B']
y1=df['D']
ax.bar(x1,y1,label ='bar')
ax.hist(x1,y1,label='hist')
ax.legend(loc='best')
#ax.scatter(x1,y1)
# x2 =np.linspace(-10,10,100)
# y2 = np.sin(5*x)
#
# ax2 =ax.twinx()
# ax2.plot(x2, y2, c='r')
#plt.figure()
#plt.hist(x=x1,bins=y1)

# plt.bar(x=df['C'], height=df['D'])
# plt.plot(x1, y1, c='r',label='haha')
# plt.scatter(x1,y1, c='y')
# plt.title('title')
# plt.xlabel('x')
# plt.ylabel('y')
#sns.lineplot(data=df, x='B',y='D')
#sns.barplot(x='B', y='D', data= df)
# plt.figure()
# sns.barplot(x='B', y='D', data= df,color='g',label='haha')

plt.show()

df =df.set_index('B')
print(df)