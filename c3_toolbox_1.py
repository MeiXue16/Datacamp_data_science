def shout(w1, w2):
    s1 = w1 + '!!!'
    s2 = w2 + '~~~'
    scon= (s1,s2)   #tuple元组
    return scon
y1, y2 =shout('haha','nana')
print(y1, y2)

import pandas as pd
daten1 = pd.read_csv('./daten_file/daten1.csv',index_col=0, nrows=20)

count ={}       #创建空字典
col =daten1['zahlen']
for i in col:
    if i in count.keys():
        count[i] +=1
    else:
        count[i] =1
print(count)

def countcol(data, col_name):
    count =dict()       #空字典
    col = data[col_name]
    for i in col:
        if i in count.keys():
            count[i] +=1
        else:
            count[i] =1
    return count

c1 =countcol(daten1, 'Nachname')
print(c1)

#Chapter 2 Default arguments, variable-length arguments and scope
#The keyword global
# Create a string: team
team = "teen titans"

# Define change_team()
def change_team():
    """Change the value of the global variable team."""

    # Use team in global scope
    global team

    # Change the value of team in global: team
    team="justice league"
# Print team
print(team)     #此时还没有调用函数，teen titans

# Call change_team()
change_team()       #调用函数
# Print team
print(team)         #justice league

#嵌套函数
def funk1(n):
    def innerfunk(word):
        x = word *n
        return x
    return innerfunk

f1 = funk1(3)('hahaa')
f2 = funk1(5)
print(f1)
print(f2('word'))


def echo_shout(word):
    """Change the value of a nonlocal variable"""
    echo_word = word * 2
    print(echo_word)
    def shout():
        """Alter a variable in the enclosing scope"""
        # Use echo_word in nonlocal scope
        nonlocal echo_word
        echo_word = echo_word + '!!!'
    # Call function shout()
    shout()
    # Print echo_word
    print(echo_word)
echo_shout('hello')  #会打印两次，一次hellohello， 一次hellohello!!!

# *args 和 **kwargs 允许您将未指定数量的参数传递给函数(*args)
# *args 用于向函数发送非关键字 可变长度参数列表 （列表）
# **kwargs 允许您将关键字 可变长度的参数传递给函数 （字典）
def gib(*args):
    n =''
    for i in args:
        n += i
    return n
word =gib('luke')
many =gib('lulu','han','nana','darth')

print(word)
print(many)

def greet(**kwargs):
    for key,value in kwargs.items():
        #.format() 三种等价表达
        #return ('{a} is {b}'.format(a=key ,b=value))
        #return('{0} is {1}.format(key, value)')
        print ('{} is {}'.format(key,value))

greet(name='yahoo', status= 'missing',age=16)

#lambda funktion
value =(lambda x,y: x*y)

v1 =value('hey',5)
print(v1)

#map()函数将给定函数应用于可迭代对象（列表、元组等）的每个项目并返回一个迭代器。
list1 =['nana', 'miya', 'eslamida', 'vier','frango','lela','froline']
var_list1 =map(lambda i: i+'~~~', list1)  #map(funktion, object)
var_list1=list(var_list1)
print(var_list1)

#filter()函数从一个iterable（列表、元组等）中提取元素，对于这些元素，函数返回True。
v2 =filter(lambda i: len(i)>5, list1)  #filter(funktion, object)
print(list(v2))

#reduce()通过将一个函数和一个可迭代对象作为参数执行传递给相邻元素的函数指定的滚动计算，并返回最终计算值。
# 第一步，选择序列的前两个元素并获得结果。
# 下一步是将相同的函数应用于先前获得的结果和第二个元素之后的数字，然后再次存储结果。
# 这个过程一直持续到容器中没有更多元素为止。
# 最终返回的结果被返回并打印在控制台上。

#reduce()函数累加滚动计算
from functools import reduce
sum1 =reduce(lambda x, y: x+y, list1)  #滚动累加计算list1中的值
print(sum1)

def funk1(word, n):
    echo_word= ''
    s_words =''
    try:
        if n < 0:
            raise ValueError('n must be greater than 0') #会被except里打印文本覆盖掉
        else:
            echo_word =word *n
            s_words =echo_word+ '~!!'
    except:
        print('word must be a string and n must be a integer!')
    finally:
        return s_words
funk1('hali', 'pote ')
print(funk1('hali', -1))
print(funk1('hali', 3))

#filter
#print(daten1['E-Mail dienstlich'])
res1 =filter(lambda x: x =='kgroten@ice.mpg.de', daten1['E-Mail dienstlich']) #筛选符合条件的列
res1 =list(res1)
for i in res1:
    print(i)


def count(daten, col='zahlen'):
    dict ={}
    try:
        col_value =daten[col]
        for i in col_value:
            if i in dict.keys():
                dict[i]+=1
            else:
                dict[i] =1
        return dict
    except:
        print('the DataFrame does not have a ',col, 'column!')

res2 =count(daten1, 'Nachname')
print(res2)
res3 =count(daten1)
print(res3)

def count2(daten, col):
    if col not in daten1.columns:
        raise ValueError('the DataFrame does not have a ',col, 'column!')
    dict ={}
    col_value =daten1[col]
    for i in col_value:
        if  i in dict.keys():
            dict[i] +=1
        else:
            dict[i] =1
    return dict

res5 =count2(daten1, 'Nachname')
print('result:',res5)

# res4 =count2(daten1, 'lang')
# print('no result:',res4)

