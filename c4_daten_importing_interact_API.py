#与API交互，从网上导入数据

#加载和探索一个JSON文件
import json

with open('a_movie.json') as file:
    data =json.load(file)       # 加载JSON文件到data中

# 打印data中的每个键值对
for k in data.keys():
    print(k, ':', data[k])

#API请求
#导入请求包
import requests

url ='http://www.omdbapi.com/?apikey=ff21610b&t=social+network'
response =requests.get(url)  #发送请求并捕获响应

print(response.text)         #打印相应内容（str格式)  .content => bytes格式

#JSON-从网页到Python
url1 ='http://www.omdbapi.com/?apikey=ff21610b&t=social+network'

response1 =requests.get(url1)

#将JSON数据解码成一个字典
data1= response1.json()

#打印data1中的每个键值对
for k in data1.keys():
    print(k, ': ', data1[k])

#检查维基百科的API
url ='https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro=&titles=pizza'

response2 =requests.get(url)

#将JSON数据解码成一个字典
data2 = response2.json()

pizza_extract =data2['query']['pages']['24768']['extract']      #字典中键的键的键的键的值
print(pizza_extract)



#深入挖掘Twitter的API
#Tweepy 是一个开源 Python 包，它为您提供了一种使用 Python 访问 Twitter API 的非常方便的方法。
# Tweepy 包含一组代表 Twitter 模型和 API 端点的类和方法，它透明地处理各种实现细节，例如： 数据编码和解码。

#API认证

import tweepy
import json
# 在相关变量中存储OAuth认证凭证
access_token = "1092294848-aHN7DcRP9B4VMTQIhwqOYiB14YkW92fFO8k8EPy"
access_token_secret = "X4dHmhPfaksHcQ7SCbmZa2oYBBVSD2g8uIHXsp5CTaksx"
consumer_key = "nZ6EA0FxZ293SxGNg8g8aP0HM"
consumer_secret = "fJGEodwe3KiKUnsYJC3VRndj7jevVvXbK2D5EiJ2nehafRgA6i"

# 将OAuth细节传递给tweepy的OAuth处理器
auth =tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#流媒体推文 Streaming tweets
#初始化流媒体监听器 Initialize Stream listener
class MyStreamListener(tweepy.Stream):
    # def __init__(self, api =None):
    #     super(MyStreamListener, self).__init__()
    #     self.num_tweets = 0
    #     self.file =open('tweets.txt', 'w')
    def on_status(self, status):
        print(status.text)
        # prints every tweet received
        # self.file.close()

    def on_error(self, status_code):
        if status_code == 420:  # end of monthly limit rate (500k)
            return False


stream =MyStreamListener('consumer_key',
                           'consumer_secret',
                           'access_token',
                           'access_token_secret')    # 初始化流媒体监听器
# stream =tweepy.Stream(auth, listener)   # 创建有认证的Stream对象

# 过滤Twitter数据流，通过关键词捕捉数据
stream.filter(track = ['clinton','trump', 'sanders', 'cruz'])


#加载并探索你的Twitter数据
import json

data3 ='tweets.txt'

tweets_data =[]

tweets_file =open(data3, 'r')
# 读取推文并存储在列表中
for line in tweets_file:
    tweet =json.loads(line)
    tweets_data.append(tweet)

tweets_file.close()

print(tweets_data[0].keys())

#Twitter data to DataFrame
import pandas as pd

df = pd.DataFrame(tweets_data, columns=['text', 'lang'])
print(df.head())

#Twitter text analysis
import matplotlib.pyplot as plt
import seaborn as sns

#set seaborn style
sns.set(color_codes =True)

list1 =['clinton', 'trump', 'sanders', 'cruz']

plt.figure()
ax = sns.barplot(data =df, x =list1, label ='[clinton, trump, sanders, cruz] ')
ax.set(ylabel ='count')
plt.show()






