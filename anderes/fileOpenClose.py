a = open('file01.txt', 'r', encoding='utf-8')
print(a.read())
a.close()

f= None
try:
    f= open('file01.txt','r',encoding='utf-8')
    print(f.read())
except FileNotFoundError:
    print('the file can not be opend')
except LookupError:
    print('Unknown code is specified')
except UnicodeDecodeError:
    print('Decoding error when reading a file')
finally:
    if f:
        f.close()

import time

#过with关键字指定文件对象的上下文环境并在离开上下文环境时自动释放文件资源
with open('file01.txt', 'r') as f:
    print(f.read())

#逐行读取
with open('file01.txt', 'r') as f:
    for line in f:
        print(line, end='')
        time.sleep(1)
print()

#按行读取到列表中
with open('file01.txt', 'r') as f:
    lines =f.readlines()
print(lines)

from math import sqrt

def is_prime(n):
    assert n>0
    for factor in range(2, int(sqrt(n))+1 ):
        if n%factor ==0:
            return False
    return True if n!=1 else False

filenames =('a.txt', 'b.txt','c.txt')
fs_list =[]
try:
    for file in filenames:
        fs_list.append(open(file, 'w'))
    for number in range(1, 10000):
        if is_prime(number):
            if number<100:
                fs_list[0].write(str(number) + '\n')
            elif number<1000:
                fs_list[1].write(str(number) +'\n')
            else:
                fs_list[2].write(str(number) + '\n')
except IOError as ex:
    print(ex)
    print('error occured!')
finally:
    for fs in fs_list:
        fs.close()
print('finished!')

#序列化：将数据从内存持久化保存到硬盘的过程
#反序列化：将数据从硬盘加载到内存

#write时， 只能写入二进制或字符串
#字典，列表，数字都不能直接写入文件中

#数据转换为字符串：repr /str 使用json模块
#数据转换为二进制：使用pickle模块
import json

name =['nana', 'miya', 'vier']
# x =json.dumps(name) #dumps方法：将数据转换为json字符串，不会保存数据
file = open('name.txt','w')
# file.write(x)
json.dump(name, file) #dump:数据转换成字符串后字节保存至file中


mydict = {
    'name': '骆昊',
    'age': 38,
    'qq': 957658,
    'friends': ['王大锤', '白元芳'],
    'cars': [
        {'brand': 'BYD', 'max_speed': 180},
        {'brand': 'Audi', 'max_speed': 280},
        {'brand': 'Benz', 'max_speed': 320}
    ]
}
try:
    with open('data.json', 'w', encoding='utf-8') as fs:
        #dump - 将Python对象按照JSON格式序列化到文件fs中
        json.dump(mydict, fs)
except IOError as e:
    print(e)
print('保存数据完成!')
# dumps - 将Python对象处理成JSON格式的字符串 serialization
# load - 将文件中的JSON数据反序列化成对象
# loads - 将字符串的内容反序列化成Python对象 deserialization
with open('data.json','r') as fr:
    p = json.load(fr)
    print(p)
fr.close()

x ='{"name":"nna", "age":18}'
new = json.loads(x)
print(new['name'])

#python 里存入数据只支持存入字符串和 二进制
#json:将python中的数据(str/ list / tuple/ list/ dict/ int/ float/ bool/ None)转换为对应的json类型
#pickle:将python中任意对象转换为二进制
import pickle
#序列化 dumps dump
#反序列化 loads load
names =['nana', 'wnawan', 'john']
#b_names = pickle.dumps(names)
# print(b_names)

file =open('names.txt', 'wb')
pickle.dump(names, file)
#file.write(b_names)
file.close()

with open('names.txt', 'rb') as f1:
     # x = f1.read()
     # y =pickle.loads(x)
     y= pickle.load(f1)
     print(y)


class Dog(object):
    def __init__(self, name, color):
        self.name =name
        self.color =color

    def eat(self):
        print(self.name +'is eating.')

d =Dog('herry', 'white')

fdog =open('dog.txt', 'wb')
pickle.dump(d, fdog)
fdog.close()

fd =open('dog.txt','rb')
dd =pickle.load(fd)
print(dd.name, dd.color)
dd.eat()

#pickle 用来将数据原封不动的转换为二进制
#json 只能保存基本类型的数据，作用是用来在不同的平台传递数据


# try:
#     file = open('hello.txt', 'r')
# except FileNotFoundError:
#     print('no file')
# else:
#     try:
#         file.read()
#     finally:
#         file.close()
try:
    with open('c.txt', 'r') as file:
        print(type(file)) #<class '_io.TextIOWrapper'>
        file.read() #不需要手动关闭文件了， with 关键字会帮我们关闭文件

except FileNotFoundError:
    print('no file')

#with: Kontext-Manager上下文管理器
#例如 文件连接，socket连接， 数据库的连接 都可以使用with自动关闭连接
#with关键字后面的对象，需要实现 __enter__和 __exit__魔法方法

#with 语句后面的结果对象，需要重写 __enter__和 __exit__方法
#当进入到with代码块， 会自动调用 __enter__方法中的代码
#当with代码块完成后， 会自动调用 __exit__方法
class Demo(object):
    def __enter__(self):
        print('__enter__方法被执行了')
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__方法被调用了')

with Demo() as d:
    print(d) # Demo() = d = Demo.__enter__() +Demo.__exit__()







import requests
import json

def main():
    resp = requests.get('http://api.tianapi.com/guonei/?key=APIKey&num=10')
    data_model = json.loads(resp.text)
    for news in data_model['newslist']:
        print(news['title'])


if __name__ == '__main__':
    main()
