import requests
from lxml import etree
import csv
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import ssl
ssl._create_default_https_context =ssl._create_unverified_context
def trans(man):
    man = ''.join(man)
    man = man.replace('\n', ' ')
    man = man.replace(',',' ')
    man = man.replace('ß', 'ss')
    man = man.replace('ä', 'ae')
    man = man.replace('Ä', 'ae')
    man = man.replace('ü', 'ue')
    man = man.replace('Ü', 'ue')
    man = man.replace('ö', 'oe')
    man = man.replace('Ö', 'oe')
    man = man.replace('é','e')
    man = man.replace('á', 'a')
    man = man.replace('ó', 'o')
    man = man.replace('š', 's')
    return man

def trans2(man):
    man = ';'.join(man)
    man = man.replace('\n', ' ')
    man = man.replace(',',' ')
    man = man.replace('ß', 'ss')
    man = man.replace('ä', 'ae')
    man = man.replace('Ä', 'ae')
    man = man.replace('ü', 'ue')
    man = man.replace('Ü', 'ue')
    man = man.replace('ö', 'oe')
    man = man.replace('Ö', 'oe')
    man = man.replace('é','e')
    man = man.replace('á', 'a')
    man = man.replace('ó', 'o')
    man = man.replace('š', 's')
    man = man.split(';')
    return man
res='./startup.html'
tree = etree.parse(res)

# result =etree.tostring(tree, encoding='utf-8').decode()
# print(result)

firmenname = tree.xpath('/html/body/div//a/text()')
firmenname = trans2(firmenname)
# print(firmenname)
firmenlink = tree.xpath('//div//a/@href')
#print(firmenlink)
liste =[]
liste.append(firmenname)
liste.append(firmenlink)
#print(liste)


def ox2dec(ox:str):
    return int(ox,16)

def decode(to_decode:str):
    decode = []
    key = ox2dec(to_decode[:2]) # 前两位为密钥
    data = []
    for i in range(2,len(to_decode),2):
        to_decode_i = ox2dec(to_decode[i:i+2])
        # print(to_decode_i,key)
        decode_i = to_decode_i^key # 十进制异或会先转二进制异或，结果再转回十进制
        decode.append(chr(decode_i)) # 十进制数转字符
    return "".join(decode)


headers={
          'Cookie': '_ga=GA1.1.1264639838.1656255816; __gads=ID=11bf5172a8fed023-22b03c0ce3cd00b6:'
                   'T=1659532896:RT=1659532896:S=ALNI_MbJBCP_xuzFH_t52bZApd1AVSs2og; _ga_0BXL4J9E2E=GS1.1.1660316184.7.1.1660317171.0',
          'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
                          'Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'

}



startjahr, adress, email, geschaftsfuhrer, facebook, webs =[], [],[],[],[],[]
date= '01.01.'
for link in firmenlink:
    response =requests.get(url=link,
                           headers=headers)
    tree2 =etree.HTML(response.content.decode())
    jahr =tree2.xpath('//div/div[1]/div/div[2]/div[1]/p/text()')
    jahr =''.join(jahr)
    jahr =date+jahr
    startjahr.append(jahr)

    kontakt =tree2.xpath('//div/div[1]/div/div[2]/div[2]/p/text()')
    adress.append(trans(kontakt))
    #print(adress)


    em = tree2.xpath('//div/div[1]/div/div[2]/div[2]/p/a/@href')
    em =''.join(em)
    em =em.split("#")[1] if '#' in em else '0'
    email.append(decode(em))
    #print(email)

    man= tree2.xpath('//div/div[1]/div/div[3]/div[2]/p/text()')
    geschaftsfuhrer.append(trans(man))
    #print(geschaftsfuhrer)

    face =tree2.xpath('//div/div[2]/div[1]/figure/a/@href')
    facebook.append(''.join(face))
    #print(facebook)

    web =tree2.xpath('//div/div[2]/div[4]/figure/a/@href')
    webs.append(''.join(web))
    #print(webs)

liste.append(startjahr)
liste.append(adress)
liste.append(email)
liste.append(geschaftsfuhrer)
liste.append(facebook)
liste.append(webs)
with open('startup_web.csv','w',newline='', encoding='utf-8') as file:
    writer =csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=';')
    writer.writerows(liste)

# for i in range(0,len(firmenlink)):
#     req =Request(firmenlink[i],
#                  headers=headers)
#     response =urlopen(req)
#     assert response.code ==200
#     with open('pages/%s.html' %i, 'wb') as file:
#         bytes_ =response.read()
#         file.write(bytes_)

# startjahr =[]
# # for i in range(0,len(firmenlink)):
# #     res ='./pages/'+ str(i)+'.html'
# #     treec= etree.parse(res)
# #     jahr = treec.xpath('/html/body//div/div[1]/div/div[2]/div[1]/p//br/text()')
# #     startjahr.append(jahr)
# #     print(jahr)


# parser = etree.HTMLParser(encoding='utf-8')
# res ='./pages/0.html'
# treec =etree.parse(res,parser=parser)
# jahr = treec.xpath('//div/div[1]/div/div[2]/div[1]/p/text()')
#em =treec.xpath('//div/div[1]/div/div[2]/div[2]/p/a/@href')
#print(em)
#startjahr.append(jahr)