import pandas as pd
import numpy as np
#读取csv文件，第0列作为索引列（可不填），输出前五行
kontact = pd.read_csv('./daten_file/contact_csv2.csv',index_col=0, nrows=10)
print(kontact['Vorname'])   #pandas series, object
print(kontact[['Vorname']]) #pandas dataframe

print(kontact.iloc[2:4])     #输出第3到4行
print('输出第3行和第6行：\n',kontact.iloc[[2,5]]) #输出第3行和第6行
print(kontact.iloc[4])      #输出第5行

print('第6行第三列的值为：\n',kontact.iloc[5,2]) #第6行第三列的值
print('第6行第三列的值为：\n',kontact.iloc[[5],[2]])#（带属性名）第6行第三列的值dataframe

print('输出第3列：\n',kontact.iloc[:,2])         #输出第3列 series
print('输出第3列：\n',kontact.iloc[:,[2]])       #（带属性名）输出第3列dataframe

print('输出Vorname和Nachname：\n', kontact.loc[:,['Vorname','Nachname']]) #输出Vorname和Nachname

# Comparison of strings
print("pyscript" == "PyScript")

# Compare a boolean with a numeric
print(True == 1)

# Comparison of strings
y = "test"
print("test" <= y)

print(True > False)

my_house = np.array([18.0, 20.0, 10.75, 9.50])
your_house = np.array([14.0, 24.0, 14.25, 9.0])

# my_house greater than or equal to 18
print(my_house >= 18 )  #每个元素都会返回一个bool值[ True  True False False]

# my_house less than your_house
print(my_house < your_house) #每个元素都会返回一个bool值[False  True  True False]

#多个条件时，要用 np.logical_**
print(np.logical_and(my_house<18 , my_house>9))
print(np.logical_or(my_house>17, my_house<10))


daten1 =pd.read_csv('./daten_file/daten1.csv',nrows=10)
sel =daten1['zahlen']
print(sel)

many_names = sel > 100
name =daten1[many_names]
print(name)

name2 =daten1[np.logical_and(sel>100, sel<200)] #多条件时，使用np.logical_and/or/xor
print(name2)

#loop
n =10
while n :
    print('n not equal to 0')
    print(n)
    n -= 1

areas = [11.25, 18.0, 20.0, 10.75, 9.50]
for i in areas:
    print(i)

for i, j in enumerate(areas):
    print('room',i+1,':',j)  #枚举函数，i:index, j:值。room 1 : 11.25

#列表循环
house = [["hallway", 11.25],
         ["kitchen", 18.0],
         ["living room", 20.0],
         ["bedroom", 10.75],
         ["bathroom", 9.50]]
for h in house:
    print('the',h[0],'is',h[1],'sqm.')

#字典循环
europe = {'spain':'madrid', 'france':'paris', 'germany':'bonn',
          'norway':'oslo', 'italy':'rome', 'poland':'warsaw', 'australia':'vienna' }

for i, j in europe.items():
    print('capital of', i, 'is',j)

#numpy multi-dimensional iterator
arr1 =np.array([[1,2,3],
                [3,4,5],
                [3,5,8]])
for i in np.nditer(arr1):       #按顺序迭代数组元素
    print(i)

#dataframe 迭代/循环
for index, row in daten1.iterrows():
    print(index)                #索引,行数
    print(row)                      #每行的内容，value

for index, row in daten1.iterrows():
    print(index,':', row['zahlen'])    #索引：值 0 : 253.4065934

for index,row in daten1.iterrows():
    daten1.loc[index,'Newcolumn']= row['Vorname'].lower() #利用迭代 添加新列

print(daten1)

daten1['newcolumn_2']= daten1['Vorname'].apply(str.lower)   #函数apply(str.lower)添加新列
print(daten1)

