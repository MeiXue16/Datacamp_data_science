#异常处理
#由于代码不规范造成程序无法正常运行，此时程序就会报错

#robust :很多编程语言都有异常处理机制

def div(a, b):
    return a/b
try:
    x=div(5,0)
    print('hahaha')
except Exception as e: #一旦程序出错，直接跳转到except语句，也就是说不打印hahaha
    print('fehler!')
else:
    print(x)

#try...except..else语句用来处理程序运行中的异常
# try:
#     file =open('ddd.txt')
#     print(file.read())
#     file.close()
# except Exception as e: #except:
#     print(e)
# except (FileNotFoundError, ZeroDivisionError) as ee:
#     print(ee)


# age =input('bitte deine Alter geben: ')
#
# try:
#     age =float(age)
# except ValueError as e:
#     print('is not number')
# else:
#     if age >18:
#         print('welcome')
#     else:
#         print('sorry')
# finally:
#     print('ende~~~~~') #最终都会被执行的代码

def demo(a,b):
    try:
        x = a/b
    except Exception as e:
        return e
    else:
        return x
    finally:
        return 'good' #会把之前的return值覆盖掉 Die finally-Anweisung überschreibt den vorherigen Return-Wert
print(demo(1,0))