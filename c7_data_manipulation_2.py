#重新排列和重塑数据
import pandas as pd
import numpy as np

# pivot_table() 函数是 pivot() 函数的泛化，它允许聚合值 aggfunc

users =pd.read_csv('./daten_file/pennsy.csv')

# Pivoting a single variable 透视单个变量
winner_pivot =users.pivot(index ='county', values='winner', columns='state')
#保存至excel表格
winner_pivot.to_excel('pivot1.xlsx')
print(winner_pivot.head())

# 不写values时，将自动为values分配除了index（行索引）和columns（列索引）的所有列
pivot2 =users.pivot(index='county', columns='winner')
print(pivot2.head())


# Stacking & unstacking
# 1.stack： 堆叠（Series-stack,宽数据 =>长数据, 等价于melt, 类似层次化的Series
# 2.unstack：unstack函数将数据从”花括号结构“变成”表格结构“,等价于pivot_table
# 3.stack和unstack默认操作为最内层
# 4.stack和unstack默认旋转轴的级别将会成果结果中的最低级别（最内层）

# DataFrame.stack(level=- 1, dropna=True)
weather =pd.read_csv('./daten_file/weather_data.csv', header=0)
weather =weather.set_index(pd.to_datetime(weather['Date'], format='%Y%m%d %H:%M'))
weather.index.name ='date'
weather.columns.name='experiment'
weather2 =weather.resample('d',label='left').mean()
print(weather2.head())

#stack()
byday =weather2.stack(level=0) #等价于level='experiment'， 把'experiment'转换为行索引
# byday2 =weather2.stack(1)        #等价于对第二层列索引堆叠，此dataframe没有第二层列索引
# byday3 =weather2.stack(level= [0,1]) #对两层列索引都进行堆叠
print('byday:\n',byday)

#unstack()
unstack_byday =byday.unstack(level= 'date')      #等价于level=0, 把date转换为列索引，长数据 => 宽数据
unstack_byday2 =byday.unstack(level='experiment') #等价于level=1,把'experiment'转换为列索引，把数据恢复成原本的表格形式
print('unstack:\n', unstack_byday2)

unstack_byday3 =weather2.unstack(level=0)       #当行索引不是复合索引时，unstack的效果类似于stack,返回一个Series
print('unstack:\n', unstack_byday3)

# 交换索引顺序（默认从内部索引开始交换）
# DataFrame.swaplevel(i=- 2, j=- 1, axis=0) 交换行索引
newusers =weather2.stack(level='experiment') #现在行索引为： date, experiment
newusers =newusers.swaplevel(i =0, j=1)     #交换第0个和第1个行索引的顺序, 现在行索引为：experiment, date
print(newusers)
# 排序，未排序的索引会导致切片失败
newusers =newusers.sort_index()
print(newusers)
#判断 newusers 是否与 byday 相等
print(newusers.equals(byday))           #false, 因为行索引顺序不同


# melt, 宽数据 => 长数据
# pandas.melt(frame, id_vars=None, value_vars=None, var_name=None, value_name='value', col_level=None, ignore_index=True)
# 添加名称以提高可读性
print(weather2.head())
#id_vars =>不变的列,  value_vars =>需要被合并的列
melt1 =pd.melt(weather2, id_vars='Temperature', var_name='其他',value_name='值')
print(melt1.head())

#设置multiindex
index1 = pd.date_range('2020-01-01', periods=365,freq='d')
users_index= weather2.set_index([index1, 'Pressure'])
#给 multiindex添加名字
users_index.index.names =['date', 'press']
print(users_index.head())

#当列标签columns有多重索引时，用col_level来选择融化的level, 0指最外层
kv_pairs =pd.melt(users_index, col_level=0)     #多重索引对melt没有任何影响，melt后的数据 索引会变成顺序索引（0~n）
print(kv_pairs)

classno=[1,1,1,2,2,2]
student=['张三','李四','王五','刘六','唐七','赵八']
chinese=[70,80,90,20,30,40]
english=[75,85,95,35,45,55]
math=   [40,50,60,70,90,80]
physcis=[45,55,65,65,75,85]
dict={'班级':classno,'学生':student,'语文':chinese,'英语':english,'数学':english,'物理':physcis}
df=pd.DataFrame(dict)
df=df.set_index(['班级','学生'])
df.columns = [['文科','文科','理科','理科'],['语文','英语','数学','物理']]
df.columns.names=['文理','科目']

#melt => 行索引会消失
df_melt =pd.melt(df, col_level=0)  #融化后只有两列： 文理（文科，理科），value
print(df_melt)

#stack 行索引保留
df_stack =df.stack(level= 1)       #会有很多NaN
df_stack =df.stack( level =[0,1])  #保留行索引的数据融化
print(df_stack)


# 设置数据透视表 pivot_table(), 使用聚合函数
# 'count' 和 len 等价
byday2 =weather.pivot_table(index='Date', columns ='Pressure', values='Temperature', aggfunc=['count',len,sum])
print(byday2)

# 在数据透视表中使用边距
# 有时在数据透视表的边缘添加总计很有用
byday3 =weather.pivot_table(index='Date', aggfunc=sum)
print(byday3)

#margins=True 最后一行添加了aggfunc(sum/np.mean/...)
byday_margin =weather.pivot_table(index='Date', aggfunc=sum, margins=True)
print(byday_margin)

