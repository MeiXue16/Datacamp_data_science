import pandas as pd

country =['spain', 'france', 'germany', 'norway']
get_index = country.index('germany')            #返回索引
print(get_index)

print(country[get_index])                       #返回索引对应的值

#dictionary
europe ={'spain':'madrid', 'france':'paris', 'germany':'berlin'}

print(europe.keys())        #返回key
print(europe.values())      #返回value

europe['poland']= 'warsaw'  #添加key-value
print(europe.get('italy','rome') ) #如果没有key 'italy',那么返回 值'rome'

print(europe)

europe['germany']='bonn'        #修改value

del europe['france']        #删除
del(europe['spain'])        #删除
print(europe)

# Dictionary of dictionaries
kontakt ={ 'nana':{'age':16, 'adress':'jena'},
           'miya':{'age':20, 'adress':'berlin'},
           'frango':{'age':40,'adress':'france'}}

print(kontakt['nana']['age'])

kontakt['frolin']={'age':19, 'adress':'bonn', 'hobby':'dance'} #添加元素
print(kontakt)

#dataframe build
names = ['United States', 'Australia', 'Japan', 'India', 'Russia', 'Morocco', 'Egypt']
dr =  [True, False, False, False, True, True, False]
cpc = [800, 730, 582, 17, 209, 74, 49]
mydict ={'country':names, 'bool':dr, 'length':cpc}

cars= pd.DataFrame(mydict)      #构造dataframe
print(cars)

row_index = ['US', 'AUS', 'JAP', 'IN', 'RU', 'MOR', 'EG']
cars.index = row_index      #添加索引行
print(cars)

cars= cars.set_index('country')     #将原本的某一列数据 修改为 索引列
print(cars)