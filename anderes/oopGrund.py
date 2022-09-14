#property装饰器
class Person(object):
    def __init__(self, name, age):
        self._name =name
        self._age = age

    # 访问器 - getter方法
    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    # 修改器 - setter方法
    @age.setter
    def age(self, age):
        self._age =age

    def player(self):
        if self._age <=16:
            print('%s playing card' %self._name)
        else:
            print('%s playing ball' %self._name)

def main():
    per1 = Person('miya', 19)
    per1.player()
    per1.age = 14
    per1.player()

if __name__ =='__main__':
    main()

from math import sqrt

class triangle(object):

    def __init__(self, a, b ,c):
        self._a = a
        self._b = b
        self._c = c
    #静态方法
    @staticmethod
    def is_valid(a, b, c):
        return a+b>c and a+c >b and b+c >a

    def perimeter(self):
        return self._a + self._b + self._c

    def area(self):
        half =self.perimeter()/2
        return sqrt(half* (half - self._a) * (half - self._b) * (half - self._c))

def main2():
    a, b , c =3, 4, 5
    if triangle.is_valid(a, b ,c):
        t =triangle(a, b ,c)
        print(t.perimeter())
        print(t.area())
    else:
        print('sorry, no triangle can be build')
if __name__ == '__main__':
    main2()

#类方法的第一个参数约定名为cls，它代表的是当前类相关的信息的对象
# （类本身也是一个对象，有的地方也称之为类的元数据对象），
# 通过这个参数我们可以获取和类相关的信息并且可以创建出类的对象

from time import time, localtime, sleep

class clock():

    def __init__(self, hour =0, minute =0, second=0 ):
        self._hour = hour
        self._minute = minute
        self._second = second

    @classmethod
    def now(cls):
        ctime = localtime(time())
        return cls(ctime.tm_hour, ctime.tm_min, ctime.tm_sec)

    def run(self):
        self._second +=1
        if self._second ==60:
            self._second =0
            self._minute +=1
            if self._minute ==60:
                self._minute= 0
                self._hour +=1
                if self._hour ==24:
                    self._hour =0

    def show(self):
        return '%02d:%02d:%02d' %(self._hour, self._minute, self._second)

def main3():
    zeit =clock.now()
    while True:
        print(zeit.show())
        sleep(1)
        zeit.run()
# if __name__ == '__main__':
#     main3()

#让一个类从另一个类那里将属性和方法直接继承下来，从而减少重复代码的编写。
# 子类除了继承父类提供的属性和方法，还可以定义自己特有的属性和方法，
# 所以子类比父类拥有的更多的能力，
# 在实际开发中，我们经常会用子类对象去替换掉一个父类对象，
# 这是面向对象编程中一个常见的行为，对应的原则称之为里氏替换原则。Richter-Ersatzprinzip
class Student(Person):
    def __init__(self, name, age, grade):
        super().__init__(name,age)
        self._grade =grade

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, grade):
        self._grade =grade

    def study(self, course):
        print('%s in %s is studying %s' %(self._name, self._grade, course))

def main4():
    stu2 = Student('nana', 18, '5 grade')
    stu2.study('programming')
    stu2.player()
if __name__ == '__main__':
    main4()

#多态
#子类在继承了父类的方法后，可以对父类已有的方法给出新的实现版本，
# 这个动作称之为方法重写（override）。
# 通过方法重写我们可以让父类的同一个行为在子类中拥有不同的实现版本，
# 当我们调用这个经过子类重写的方法时，不同的子类对象会表现出不同的行为，
# 这个就是多态（poly-morphism）。
#Wenn eine Unterklasse eine Methode von der Elternklasse erbt,
# kann sie die Methode der Elternklasse neu implementieren,
# was man als Methodenüberschreibung bezeichnet.
# Indem wir eine Methode überschreiben, können wir dafür sorgen,
# dass dasselbe Verhalten der Elternklasse in der Kindklasse unterschiedlich implementiert wird,
# so dass sich verschiedene Objekte der Kindklasse unterschiedlich verhalten,
# wenn wir die überschriebene Methode aufrufen.
from abc import ABCMeta, abstractmethod

class Pet(object, metaclass= ABCMeta):
    def __init__(self, nickname):
        self._nickname = nickname

    @abstractmethod
    def make_voice(self):
        pass

class Dog(Pet):
    def make_voice(self):
        print('%s: wang wang wang'%self._nickname)

class Cat(Pet):
    def make_voice(self):
        print('%s: miao miao miao'%self._nickname)

def main():
    pets = [Dog('John'), Cat('Kartin')]
    for i in pets:
        i.make_voice()

if __name__ =='__main__':
    main()

