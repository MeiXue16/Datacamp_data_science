import numpy as np
import matplotlib.pyplot as plt
#random float

# import random
# random.seed(10)     #随机数生成器需要一个数字开头（种子值），才能生成随机数。
# print(random.random())
#
# random.seed(10)
# print(random.random())  #如果您两次使用相同的种子值，您将获得两次相同的随机数

#set the seed
np.random.seed(100)
print(np.random.random(4)) #生成4个随机数
print(np.random.rand(4,2))  #生成4*2的随机数组，np.random.rand()可以生成多维随机数组

np.random.seed(8)
print(np.random.randint(1,7)) # 使用randint()来模拟一个骰子 1-6
print(np.random.randint(1,7))

step =50
while step<100:
    dice= np.random.randint(1,7)
    if dice <=3:
        step -=1
    else:
        step +=1
    # print(dice,'step:',step)
print(step)

#初始化random walk
rw =0

for i in range(10):
    step = np.random.randint(1,7)
    rw +=step
    print('randomc walk step',i,',',step,':', rw)

#random walk列表
rwlist =[0]
np.random.seed(14)
for i in range(20):
    position =rwlist[-1]

    dice =np.random.randint(1,7)
    if dice<=3:
        position = max(0, position-1)
    if dice<=5:
        position +=1
    else:
        position +=np.random.randint(1,7)
    rwlist.append(position)
print(rwlist)

#画图
plt.figure()
plt.plot(rwlist)  #x为列表索引（0-19），y为列表值
#plt.show()

#模拟十次 15步的 random walk
np.random.seed(20)
multiwalk =[]
for i in range(10):
    rw= [0]
    for j in range(15):
        posi =rw[-1]
        dice =np.random.randint(1,7)
        if dice <=2:
            posi -=1
        elif dice <=5:
            posi +=1
        else:
            posi += np.random.randint(1,7)

        rw.append(posi)
    multiwalk.append(rw)
print(multiwalk)

arr1 =np.array(multiwalk)
print(arr1)
#画图
plt.figure()
plt.plot(arr1)
#plt.show()
plt.clf() #清理图片，这样就不用再新建画布

arr2 =arr1.T  #转置
print(arr2)

arr3 =np.transpose(arr1) #转置 与arr1.T 效果一样
plt.plot(arr3,label='arr3')
plt.title('array3')
plt.legend(loc='best')
#plt.show()

end =arr3[-1, :]  #最后一行
plt.figure()
plt.hist(end)  # 画直方图 Plot histogram of ends
plt.show()
