#zahlen
b, c =3.5, 4e+01
print(c**b)  #c^b
print(c%b) #c mod b
print(c//b)  #int(c/b)

d= 2+3j
print(d.real)
print(d.imag)

print('I\nLove\nApple') #Zeilenvorschub

pi_string ='3.1415926'
pi_float =float(pi_string)
pi_string=str(pi_float)
print('pi =' + str(pi_float))
print('pi =', pi_float)

print('bitte eine ganze Zahl eingeben: ')
#a= int(input())             #input

#list
list1 =list()
list1.append(2)
list1.append(3.3)
print(list1) #[2, 3.3]

list1.remove(3.3) #删除
print(list1) #[2]

list2 = [1,10,'python',['b',[1,33]]]
print(list2[3][1][1])  #33

list2.pop() #弹出并删除最后一个值
print(list2) #[1, 10, 'python']
print(list2*2) #[1, 10, 'python', 1, 10, 'python']

del(list2[2])  #按索引位置删除
print(list2)
#set
s={1,1, 2,3,3,4,0,1,0}
print('s: ',s)
print('type of s: ', type(s)) #数据类型

a=set(list1)
#print('a: ',a)

a.add(5)
a.discard(1) #删除不存在的元素，也不会报错
a.remove(2)
print('a: ', a)

#dictionary
d =dict()
print(d)

dic ={'name':'nana','alt':'26', 'wohnung':'jena', 'country':'china'}
print(dic)

dic['alt']=30
dic['country']= 'germany' #修改
dic['telefon']= '1585076' #添加新元素

del dic['wohnung'] #删除
print(dic)
print(dic.get('alt'))   #获取
print(dic.get('wohnung','berlin')) #添加新元素

#methods
list3 =[1,9,100,4,5,2,3,8,3]
list4 =[33,4,1,2,45,6,3,5,8,0,3]
list3_sorted= sorted(list3,reverse= True) #降序排序 [100, 9, 8, 5, 4, 3, 3, 2, 1]
print(list3_sorted)

list4.sort(reverse=True) #降序排序
print(list4)

print('index of first 3:', list4.index(3))   #数字3所在的位置
print('how ofen 3 appears: ',list4.count(3))  # 3出现的次数
list4.append(90)
list4.reverse() #顺序颠倒
print(list4)

list5=[1,6,3,7,1,0,3,5,3]
print(list5[::-1]) #顺序颠倒
print(list5[2::-1]) #[3, 6, 1]顺序颠倒读取到索引位置为2的元素

#string
room='miaomiao HHHA world'
print(room.upper()) #大写
print(room.lower()) #小写
print(room.capitalize()) #首字母大写
list5_str= str(list5)  #转换为string
print('string format of list5:', list5_str) #[1, 6, 3, 7, 1, 0, 3, 5, 3]

room= room.replace(' ','%') #替换空格为 %
print(room[6])
room=list(room) #转换为列表
print(room)
print(room[6])
room = '-'.join(room) #将列表元素用‘-’链接起来
print(room)

#package math 数学函数包
import math as m
c =2 *0.34 * m.pi  #pi来源于math包
dist = 10 * m.radians(30) #将不同的度数转换为弧度Convert different degrees into radians
print(dist)
drgree =m.degrees(m.pi) #将弧度转换为度数
print(drgree)

#Numpy  科学计算基础包 Numerical Python
import numpy as np
print(np.sin(m.pi/2)) #sin()函数
x =np.array(list4)  #列表转换为数组
print(x)
y= np.array([4,5,6]) #创建数组
print(y)
y2=np.array([1,2,3])

print(y + y2)  #长度一致的数组才能相加 [5 7 9]
print(y**2)    #元素平方 [16 25 36]

print(np.dot(y, y2)) #内积 32
print(2 * y2)  # 2 * [1,2,3] = [2 4 6]
print(y * y2)  #同行列元素相乘 [ 4 10 18]

print(np.cross(y ,y2))  #叉积/向量积 kreuzprodukt [ 3 -6  3]
print(np.outer(y, y2))  #外积 Dyadisches Produkt y(y2)^T
# [[ 4  8 12]
#  [ 5 10 15]
#  [ 6 12 18]]

arr1= np.outer(y, y2)
light = arr1 <15  #bool数组
print(light)

print(arr1[2]) #返回数组第三行

arr2 =np.array([
                [1,2,3],
                [4,5,6],
                [7,8,9]
              ])         #生成二维数组
print(arr2)

arr3 =np.matrix('1 2 6;\
                 3,6,3;\
                 4,7,9')
print(arr3)            #生成二维数组/矩阵

print(arr2.T)   #转置
print(np.dot(arr2, arr3))  #矩阵乘法
print(arr3+arr2)            #矩阵加法

print(arr3.shape)       #数组维度 (3, 3)

print(arr3[1,1])        #第二行第二列：6
print(arr3[:,1])        #所有行，第二列

print(np.mean(arr3[:,0]))        #返回第一行的均值2.6666666666666665
med =np.median(list(arr3))
print(med)                       #一定要把matrix转换成list,才会生成中位数
print(np.median(arr2))             #array的中位数
print(np.std(arr3))             #标准差
print(np.var(arr3))             #方差

print(np.corrcoef(arr2[:,0], arr2[:, 1])) #第一列和第二列之间的相关系数


