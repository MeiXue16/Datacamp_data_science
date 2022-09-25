#从网络中获取数据：数据爬虫
import csv
from urllib.request import urlretrieve
import pandas as pd

#指定文件的网址
url ='https://s3.amazonaws.com/assets.datacamp.com/production/course_1606/datasets/winequality-red.csv'

#把文件保存到本地
urlretrieve(url, 'wine.csv')

# 读取文件到DataFrame并打印其前五行
df5 =pd.read_csv('wine.csv', sep=';')
print(df5.head())

# 从网络上打开并读取flat文件前五行
df6 =pd.read_csv(url, sep=';')
print(df6.head())


import matplotlib.pyplot as plt
import pandas as pd
plt.figure()
plt.hist(df6.iloc[:,[0]])       #用df6第一列数据画直方图，也可以写作plt.hist(df6.iloc[:,0])
plt.xlabel('fixed acidity (g(tartaric acid))')
plt.ylabel('count')
# plt.show()

# Assign url of file: url
url2 = 'http://s3.amazonaws.com/assets.datacamp.com/course/importing_data_into_r/latitude.xls'

# 读取Excel文件的所有工作表
import xlrd
x1 =pd.read_excel(url2,sheet_name=None)  #一定要设置sheet_name=None,不然会默认读取第一张工作表
print(x1.keys())                    #返回所有工作表的表名: dict_keys(['1700', '1900'])

print(x1['1700'].head())            #返回第一张工作表的前五行


#使用urllib在Python中执行HTTP请求
from urllib.request import urlopen, Request

url3 ='http://www.datacamp.com/teach/documentation'
headers={
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)'
                 ' Version/13.0.3 Mobile/15E148 Safari/604.1',
    'Cookie':'IR_gbd=datacamp.com; dc_consent={"version":"1.0.0","essential":1,"functional":1,"performance":1,"advertisement":1}; _gcl_au=1.1.1878465066.1662303917; _ga=GA1.2.123712248.1662303915; _mkto_trk=id:307-OAT-968&token:_mch-datacamp.com-1662303918471-48948; _fbp=fb.1.1662303918745.480354868; smc_tag=eyJpZCI6NDQ1NCwibmFtZSI6ImRhdGFjYW1wLmNvbSJ9; smc_session_id=KoKwkPHEheD6LECDqEJzDWYff71HeBKf; smc_uid=1654776815539437; cb_user_id=null; cb_group_id=null; cb_anonymous_id=%22d4eecd9d-3b3e-442d-8968-aa7a673cda9e%22; smc_sesn=1; _hjSessionUser_2445625=eyJpZCI6ImYyMTBlNGYxLTAwYTUtNWYzZi1iYTI4LWYwNDVhMDI2ZjAwNSIsImNyZWF0ZWQiOjE2NjIzMDM5MTk4MjgsImV4aXN0aW5nIjp0cnVlfQ==; _hjSessionUser_2898792=eyJpZCI6IjViNWNmZDkxLWM2NjgtNWMxMy1iMmE0LTk1OWJmZDNlMDdiYyIsImNyZWF0ZWQiOjE2NjIzMDQ0MTA2NTcsImV4aXN0aW5nIjp0cnVlfQ==; _hjSessionUser_1719197=eyJpZCI6ImQ2NTNmMTllLTllNDItNTBkZS05YWMxLWNhYjVhY2FhNTJhMCIsImNyZWF0ZWQiOjE2NjIzMDg1MzgxMzEsImV4aXN0aW5nIjp0cnVlfQ==; smc_not=default; _hjSessionUser_484663=eyJpZCI6ImE1NWE5NzA3LWE4NjUtNTc0Yy04YmUyLTEyYjQ0Y2UyODE0ZCIsImNyZWF0ZWQiOjE2NjI5MzU5NTQyMDAsImV4aXN0aW5nIjpmYWxzZX0=; dc_pricing_currency=EUR; smc_v4_86304=%7B%22timer%22%3A0%2C%22start%22%3A1662935955151%2C%22last%22%3A1662935955151%2C%22disp%22%3A1662935970454%2C%22close%22%3Anull%2C%22reset%22%3Anull%2C%22engaged%22%3Anull%2C%22active%22%3A1662935968630%2C%22cancel%22%3Anull%2C%22fm%22%3Anull%7D; _dct=eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL3d3dy5kYXRhY2FtcC5jb20iLCJqdGkiOiIxMTU4MzM2Mi0zMzk5N2Y5NmRlNTk5NTZmMGRhNzYzYjVjZGI3N2IxY2QwMmM1ODgyOGY3NzhkNzNmNzJlOTYyZGVmMjYiLCJ1c2VyX2lkIjoxMTU4MzM2MiwiZXhwIjoxNjcwNzk4NzYzfQ.EmVyDLwWIrHqFHwpkQwkBk62Tju9VQvORVoZcKx4dzw2XJDb-4meIizvRKXZtBbo3khfY3NN6grsZSJgCpoa7CdCy8bKkrJQjOl2bJp1rPlPmItQwfK4KOukiM9ukToTD746SZB3fX26ccH0w1qAqW72aOFLdUTlrM_LGB5_AzI_xK8L76gbqGduxe2Ny9E5S5d65xW4RbxKx7Utb5_I05xW8YfofxTCQY6J4grj0YHDYxBTwbX9_1oaRDjHB_ne6WocT3XPiXVFRU7ikfci9AeG63bgDB7TtZirQIiOmYrLqRvfWEfwSeMez8O8Zwwe6wDRNwcsyTFFhXkZZaI8xg; _cioid=11583362; IR_13294=1662937926060%7Cc-25240%7C1662937926060%7C%7C; IR_PI=39b2c8c3-11ee-11ed-bf2a-e389691024cc%7C1663024326060; smc_v4_86310=%7B%22timer%22%3A0%2C%22start%22%3A1662477154397%2C%22last%22%3A1662477154397%2C%22disp%22%3A1662478053472%2C%22close%22%3Anull%2C%22reset%22%3Anull%2C%22engaged%22%3Anull%2C%22active%22%3A1663150774099%2C%22cancel%22%3Anull%2C%22fm%22%3Anull%7D; _gid=GA1.2.358215904.1663842039; _hp2_props.4292810930=%7B%22Signed%20In%22%3A%22true%22%2C%22Promo%20Active%22%3A%22true%22%2C%22Active%20Promos%22%3A%22data_literacy_2022%22%7D; _hp2_id.4292810930=%7B%22userId%22%3A%224767561761137445%22%2C%22pageviewId%22%3A%228513247258062237%22%2C%22sessionId%22%3A%22148441662990248%22%2C%22identity%22%3A%2211583362%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%2C%22oldIdentity%22%3Anull%7D; _uetsid=34b311203a6011eda0c59fd252c14900; _uetvid=4aafc680539711ec98dcd518502051eb; smc_tpv=146; smc_spv=146; smct_last_ov=%5B%7B%22id%22%3A89265%2C%22loaded%22%3A1663878141912%2C%22open%22%3Anull%2C%22eng%22%3Anull%2C%22closed%22%3Anull%7D%2C%7B%22id%22%3A86310%2C%22loaded%22%3A1663150773121%2C%22open%22%3Anull%2C%22eng%22%3Anull%2C%22closed%22%3Anull%7D%2C%7B%22id%22%3A86304%2C%22loaded%22%3A1662935965486%2C%22open%22%3A1662935970452%2C%22eng%22%3Anull%2C%22closed%22%3Anull%7D%5D; _sp_id.6552=002dc7ef-3667-4695-bd4d-d7b157b3be4f.1662303911.25.1663878143.1663842044.c06cff8f-f4b2-44e7-b864-58c60f73170f; smc_v4_89265=%7B%22timer%22%3A0%2C%22start%22%3A1663325759125%2C%22last%22%3A1663325759125%2C%22disp%22%3Anull%2C%22close%22%3Anull%2C%22reset%22%3Anull%2C%22engaged%22%3Anull%2C%22active%22%3A1663878142918%2C%22cancel%22%3Anull%2C%22fm%22%3Anull%7D; __cf_bm=IbbOipqWdxw3hvlFEnUu67cwz50oIyfrcyTEaBs2Szg-1663881699-0-ARXetDOUvqqGpTYbOAKr9ZRhTN+vZSgoR0fKwFrmbY47znwjaRPbDMKM2J/GG1FozugsvWhVr/DB4ExBIGPAVPvu8f8dBD/LCYzdRAoc6lwrutKzvgLdKXCKi394h09+K7XADERskq7zERESbW7EhDsy8R9ZuZ7ScbA2xkP3SR07; intercom-id-ug0ps1rq=5049f61d-3933-4e53-88e0-d3dec2f2b341; intercom-session-ug0ps1rq=; smct_session=%7B%22s%22%3A1662993598885%2C%22l%22%3A1663882058858%2C%22lt%22%3A1663882058859%2C%22t%22%3A2578%2C%22p%22%3A2579%7D'
}

req =Request(url= url3,headers= headers)      #更多知识可以看doubanDatenCrawlen.py

response =urlopen(req)  # 发出请求并捕获响应

assert response.code ==200
# print(type(response))
with open('page.html', 'wb') as file:  #以二进制读写打开file:'page.html'
    bytes_ =response.read()             #读取响应内容
    file.write(bytes_)                  #写入file中
print('download der page erfolgreich!')

# print(type(response))       #<class 'http.client.HTTPResponse'>
response.close()                #关闭响应


#使用urllib在Python中打印HTTP请求结果
from urllib.request import urlopen, Request

url4= 'https://www.bilibili.com/read/cv10222110'
req2 =Request(url4)     #请求
response2 =urlopen(req2)    #响应

with open('page2.html', 'wb') as file2:
    p2 = response2.read()
    file2.write(p2)

response2.close()

#用BeautifulSoup解析HTML
import requests
from bs4 import BeautifulSoup

url5 ='https://www.python.org/~guido/'
response3 = requests.get(url5)      # 将请求打包，发送请求并捕获响应

html_doc = response3.content      # 将响应提取为bytes格式. 将响应提取为str格式用 response3.text;
print(type(html_doc))           # <class 'bytes'>

soup = BeautifulSoup(html_doc,'html.parser') # 解析HTML代码 soup = BeautifulSoup(html_doc) 效果也一样
pretty_soup = soup.prettify()   #prettify()方法将把Beautiful Soup解析树变成一个格式良好的Unicode字符串，每个标签和每个字符串都有一个单独的行。
print('type of pretty_soup',type(pretty_soup))
with open('soup1.html','w') as file3:
    file3.write(pretty_soup)        #将pretty_soup保存至文件soup1.html中


# 使用BeautifulSoup将网页变成数据：获取文本
from bs4 import BeautifulSoup #beautifulsoup4
import requests

url6 ='https://www.geeksforgeeks.org/pretty-printing-in-beautifulsoup/'
headers2 ={
    'User-Agent':'',
    'Cookie':''
}

response4 =requests.get(url6, headers=headers2)
soup2 =BeautifulSoup(response4.text, features="html.parser")

print(soup2.title) #<title>Pretty-Printing in BeautifulSoup - GeeksforGeeks</title>
text1 = soup2.get_text()
print(type(text1)) #<class 'str'>
with open('soup2.txt', 'w',encoding='utf-8') as file4:
    file4.write(text1)


#使用BeautifulSoup将网页变成数据：获得超链接
import requests
from bs4 import BeautifulSoup

url7 ='https://www.bilibili.com/video/BV1tf4y117Sh/?p=20&spm_id_from=pageDriver'
response5 =requests.get(url7)
soup3 =BeautifulSoup(response5.content, 'html.parser')
print(soup3.title)                      #打印网页标题 <title data-vue-meta="true">S01E09.b.格式之日期和时间_哔哩哔哩_bilibili</title>

a_tags = soup3.find_all('a')            # 找到所有'a'标签（定义超链接）：a_tags
print('type of a_tags',type(a_tags))    #<class 'bs4.element.ResultSet'>
list1=[]
for link in a_tags:
    list1.append(link.get('href'))      #循环打印出a_tags中 （key）href对应的（value）链接

import pandas as pd
df1 =pd.DataFrame(list1)
df1.to_csv('df2csv.csv',encoding='utf-8')   #用dataframe将数据转存为csv

with open('soup3_hyperlink.csv', 'w',newline='') as file5:
    writer =csv.writer(file5)
    writer.writerow(list1)               #用csv.writer方法将列表转入csv,这为一行数据。

# 不用for循环：（[[1,2,3],[4,5,6]] 时用writerows, 会得到3行数据）


