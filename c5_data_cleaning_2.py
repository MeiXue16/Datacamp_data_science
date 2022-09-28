# 合并数据进行分析
import pandas as pd

df1 =pd.DataFrame([['a',1], ['b',2]], columns=['letter', 'number'])
df2 =pd.DataFrame([['c',3], ['d',4]], columns=['letter','number'])
# 类似 outer join/ append， 因此注意表头/列名要一致
# concat默认纵向连接DataFrame对象， 并且合并之后不改变原本DataFrame子对象的index值
concat1 = pd.concat([df1,df2])
print(concat1)

# 忽略原本的Index值
concat1 = pd.concat([df1,df2], ignore_index= True)
print(concat1)

df3 = pd.DataFrame([['c', 3, 'cat'], ['d', 4, 'dog']],
                  columns=['letter', 'number', 'animal'])

# 表头不完全一致时：使用 join= 'inner'可以只显示并合并相同列
# sort=False : 列的顺序维持原样， 不进行重新排序
concat2 =pd.concat([df1, df3], sort= False, join= 'inner')
print(concat2)

#横向合并 axis = 1
df4 =pd.DataFrame([['cat',2], ['dog', 5]], columns= ['animal','no.'])
concat3 =pd.concat([df1, df4], axis = 1)
print(concat3)

#打印concat3 的形状
print(concat3.shape)


#glob是python自己带的一个文件操作相关模块，用它可以查找符合自己目的的文件，
# 类似于Windows下的文件搜索，支持通配符操作
import glob
pattern1 ='../*.csv' #父目录下的所有csv文件，不包括父目录的子文件夹中的内容

#绝对路径
pattern2 ='F:/Master_studium/master1.6/兼职工作内容/15 联系人表格/*.csv'

#相对路径，父目录下的子文件夹daten_file中 的csv文件
pattern3 ='./daten_file/*.csv'

#结尾为数字的csv文件
pattern ='./daten_file/*[0-9].csv'

#结尾为数字的所有类型的文件
pattern5 ='./daten_file/*[0-9].*'

# 保存所有匹配的文件,glob方法返回所有匹配的文件路径列表
# * =>多个字符， ? => 一个字符， [0-9] => 指定数字范围 ， [?] =>匹配字符 “?”
csv_files= glob.glob(pattern)
print(csv_files)

# 迭代和串联所有匹配的内容
frames =[]
for csv in csv_files:
    #将csv转化为dataframe
    df =pd.read_csv(csv)
    #将df加入列表frames
    frames.append(df)

#将frames合并成一个单一的DataFrame。若只显示联合的相同表头：join='inner'
join1 =pd.concat(frames,
                 ignore_index= True)
print(join1.head())


# 1对1的数据合并,左右拼接
#pd.merge()的作用是用数据库样式的连接合并DataFrame或者已命名的Series。
#pd.merge( left, right, how='inner', on=None, left_on=None, right_on=None,
# left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=True, indicator=False, validate=None,)

#和pd.concat()不同，pd.merge()只能用于两个表的拼接，而且通过参数名称也能看出连接方向是左右拼接，一个左表一个右表，而且参数中没有指定拼接轴的参数，
# 所以pd.merge()不能用于表的上下拼接。

#默认是inner join, left=左边的dataframe, right=右边的dataframe, on=连接key列
df1_m_df2 =pd.merge(left= df1, right= df2, on ='letter')

#外连接
df1_m_df2 =pd.merge(left= df1, right= df2, how='outer',on ='letter')

#左连接
df1_m_df2= pd.merge(left =df2, right=df3, how='left',on='number')


#索引连接 left_index right_index, 使用左右两张表对应的索引进行连接
df1_m_df2 =pd.merge(left= df1, right=df3, left_index=True, right_index=True)

#当左右两张表的join on key列名不一致时：left_on =.. right_on= ..
df1_m_df2 =pd.merge(left =df1, right= df4, how='outer',left_on='number', right_on='no.')
print(df1_m_df2)

import numpy as np
#type()    返回参数的数据类型
#dtype    返回数组中元素/ dataframe某列元素 的数据类型
#dtypes      返回dataframe中所有列的数据类型
#astype()    对数据类型进行转换

#转换 某列 数据类型
#将dataframe df3的number列数据类型转换为float
df3.number =df3.number.astype('float')

#打印某列数据类型
print(df3.number.dtype)

#转换 整个数据集 的数据类型
df5 =df3.astype('category')     #分类类型

#打印所有列的数据类型
print(df5.dtypes)

#打印详细数据信息
print(df5.info())

#infer_objects
# Infer dtypes of objects.
#
# to_datetime
# Convert argument to datetime.将参数转换为日期时间
#
# to_timedelta
# Convert argument to timedelta.将参数转换为时间点。
#
# to_numeric
# Convert argument to a numeric type.将参数转换为数字类型。
# errors{‘ignore’, ‘raise’, ‘coerce’}, default ‘raise’
# If ‘raise’, then invalid parsing will raise an exception.则无效解析将引发异常。
# If ‘coerce’, then invalid parsing will be set as NaN.无效解析将被设置为NaN。
# If ‘ignore’, then invalid parsing will return the input.则无效解析将返回输入。
df3.letter =pd.to_numeric(df3['letter'], errors ='coerce')
print(df3)


#用正则表达式进行字符串解析
#导入正则表达式模块
import re

# . 除了换行的任意字符， a.*b，应用于aabab会匹配整个字符串aabab
# ^ 匹配字符串的开头, 在MULTILINE 模式也匹配换行后的首个符号,^The可以匹配The开头的字符串
# $ 匹配字符串的结束，z.B. cat$ 只能匹配cat结尾的字符串, 不能匹配cat is cute.
# * 0~n, 任意多个字符
# ? 0~1, z.B. nab? , 只能匹配na, nab
# + 1~n次重复, z.B. wan+, 只能匹配wan,wann,wannn....
# *? 非贪婪模式，其中的?能够最小化匹配, Z.B.a.*?b 应用于aabab，会匹配aab和ab两个字符串。<.*?>应用于 <a> b <c>,只能匹配<a>
# {n} n次重复，z.B. miao{4}x 只能匹配miaoooox, miaooooox,...
# {m,n} m~n次重复，z.B. a{3, }b 匹配aaab,aaaaaaaaaaab
# {m,n}? 非贪婪模式，只匹配尽量少的字符次数。z.B. a{3,5}? 只匹配3个 'a'
# \ 转义字符，允许你匹配 '*', '?'...
# r"\cs",r可以使反斜杠不必做任何特殊处理， 这里 \cs 表示一个反斜杠和cs字符
# [], 表示集合：z.B. [amk]匹配 'a','m'或者 'k'. [a-z] 将匹配任何小写ASCII字符. [0-5][0-9] 将匹配从 00 到 59 的两位数字. [0-9A-Fa-f] 将匹配任何十六进制数位。[(+*)] 只会匹配这几个字面字符之一 '(', '+', '*', or ')'。
# [^], 取反， 匹配不在字符集中的任意单一字符，[^aeiou] 可以匹配任一非元音字母字符
# \w 匹配字母/数字/下划线,z.B. b\wt, 可以匹配 bat / b1t / b_t等, 但不能匹配b#t
# \W 匹配非字母/数字/下划线,z.B.b\Wt 可以匹配b#t / b@t等,但不能匹配but / b1t / b_t等
# \d 匹配数字,z.B. \d\d 可以匹配01 / 23 / 99等
# \D 匹配非数字,z.B. \d\D 可以匹配9a / 3# / 0F等
# \b 匹配单词的边界,z.B.\bThe\b
# \B 匹配非单词边界, z.B. \Bio\B
# \S 匹配非空白字符,z.B. love\Syou 可以匹配love#you等,但不能匹配love you
# | 分支，z.B. foo|bar 可以匹配foo或者bar
#(?#) 注释
# (exp) 匹配exp并捕获到自动命名的组中， (?<name>exp)匹配exp并捕获到名为name的组中
# (?:exp)匹配exp但是不捕获匹配的文本
# (?=exp)匹配exp前面的位置， \b\w+(?=ing)可以匹配I'm dancing中的danc
# (?<=exp) 匹配exp后面的位置，(?<=\bdanc)\w+\b可以匹配I love dancing and reading中的第一个ing
# (?!exp) 匹配后面不是exp的位置
# (?<!exp) 匹配前面不是exp的位置
# re.I / re.IGNORECASE 忽略大小写匹配标记
# re.M / re.MULTILINE 多行匹配标记

# 编译该模式
prog = re.compile('\d{3}-\d{3}-\d{4}')
result = prog.match('123-456-7899')
print('result: ',bool(result))
print(result)
#等价于
result = re.match('\d{3}-\d{3}-\d{4}', '123-456-7891')
print('result: ',bool(result))
print(result)

# findall(pattern, string, flags=0)查找字符串所有与正则表达式匹配的模式, 返回字符串的列表
# 匹配所有 重复1~n次的数字
result2 =re.findall('\d+', 'i have 5 dogs and 10 cats.')
print(result2)

# match(pattern, string, flags=0)用正则表达式匹配字符串 成功返回匹配对象, 否则返回None
# 匹配字符串’$number.numbernumber‘
result3 =re.match('\$\d*\.\d{2}', string='$123.456')
print(result3)  #match='$123.45'

result4 =re.match('[A-Z]\w*', 'Australia')
print(bool(result4))

#自定义函数来清理数据
#定义recode_sex()
def recode_sex(value):
    if value =='Male':
        return 1
    elif value =='Female':
        return 0
    else:
        return np.nan

df3 =df3.astype('str')
df3['gender']= ['Male','Female']
# 将该函数应用于性别列
df3.gender =df3.gender.apply(recode_sex)
print(df3)

#Lambda函数
#用替换法编写λ函数
df3['letter']= ['$a$b$$$c', 'h$c$0']
#把所有$符号都替换为空字符''
df3['letter']= df3.letter.apply(lambda x: x.replace('$',''))
print(df3)

df3.number =['32.53.098', '130.776' ]
#返回第一个满足 数字.数字的字符串
df3.number= df3.number.apply( lambda x: re.findall('\d+\.\d+', x)[0])
print(df3)


#删除重复的数据
df3 =df3.drop_duplicates()

# 填补缺失的数据
#转换数据类型
df3.number =pd.to_numeric(df3.number, errors= 'coerce')
# 计算均值 np.mean(df3.number)/ np.mean(df3['number'])
mean1 =df3.number.mean()
df3.letter =pd.to_numeric(df3.letter, errors='coerce')

#把letter列的所有缺失值用number列的均值替换掉
df3.letter =df3.letter.fillna(mean1)
print(df3)

#用断言测试你的数据

#打印对象是否为null/na，bool矩阵
print(pd.notnull(df3))
print(pd.notna(df3))

# assert断言没有缺失值
# 若断言正确，则控制台没有任何返回。 若断言错误，返回断言错误（AssertionError）
assert pd.notnull(df3).all().all()
assert (df3.number <=0).all().all()