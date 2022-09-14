#系统内置异常
#ZeroDivisionError:
# 1/0
# #FileNotFoundError
# open('nnnn.txt')
# # ValueError
# int('hello')
# # FileExistsError 多次创建同名文件
# os.mkdir('test')
# KeyError
# person ={'name':'nana'}
# person['age']
#
# IndexError
# name =['zhangsan', 'nana']
# name[5]

#SyntaxError 语法错误，例如中文字符，没加冒号

#自定义异常
#要求：让用户输入用户名和密码，如果长度在6-12位则正确，否则报错
class MyError(Exception):
    def __init__(self, min,max):
        self.min =min
        self.max = max
    def __str__(self):
        return 'the length must be between {} and {}'.format(self.min, self.max)

password =input('password geben:')
if 6<= len(password) <=12:
    print('richtig password')
else:
    raise MyError(6,12)
    #raise ValueError('falsch password')
    #使用raise 关键字抛出异常
