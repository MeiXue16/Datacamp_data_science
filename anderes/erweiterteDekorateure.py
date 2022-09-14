# def can_play(fn):
#     print('externe funktion ist aufgerufen')
#     def inner(name, game, **kwargs): # kwargs ={'clock':22}字典 kwargs['clock'] 但是如果没有参数传过来，这样写会报错， 用get不报错
#         clock = kwargs.get('clock', 21)
#         if clock>21:
#             print('zu spaet, kann nicht spielen')
#         else:
#             fn(name,game)
#
#     return inner
#
# @can_play #装饰器
# def play_game(name, game):
#     print(name + ' playing '+ game)
# #play_game函数是 can_play的参数 fn, fn =play_game
# play_game('nana', 'mobile legends')
# play_game('maya', 'bigballeatsmallball',clock=22)

#高级装饰器
def can_play(clock):
    print('externe funktion ist aufgerufen')
    def handle_action(fn):
        def do_action(name, game):
            if clock< 21:
                fn(name ,game)
            else:
                print(name +' zu spaet, kann nicht spielen'+ game)
        return do_action
    return handle_action
#调用can_play函数，将参数 12传递给clock变量，
#再调用handle_action函数
@can_play(22)
#将play_game传递给 fn
def play_game(name, game):
    print(name + ' playing '+ game)
#此时调用play_game其实就是调用do_action
play_game('viecent', 'tiktok')






#user_permission =9  # 0b111
user_permission =12 # 2^4 -1 =15 共15个可能
#权限因子
DEL_PERMISSION =8 #   1000
READ_PERMISSION =4  # 0100 二进制
WRITE_PERMISSION =2 # 0010
EXE_PERMISSION =1   # 0001

def check_permission(x,y):
    #print('user permission %d externe funktion ist aufgerufen'%x)

    def handle_action(fn):
        def do_action():
            if x & y !=0: #按位与运算
                fn()
            else:
                print('sorry, no zugang')

        return do_action
    return handle_action

@check_permission(user_permission, READ_PERMISSION)
def read():
    print('I am reading')

@check_permission(user_permission, WRITE_PERMISSION)
def write():
    print('I am writing')

@check_permission(user_permission, EXE_PERMISSION)
def execute():
    print('I am executing')

@check_permission(user_permission, DEL_PERMISSION)
def delete():
    print('I am deleting')

read()
write()
execute()
delete()

#开放封闭原则 OCP，Open Closed Principle