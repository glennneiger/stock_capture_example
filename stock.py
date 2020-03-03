#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import operator
import time
import datetime
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

HSIIndexLists = []
url = 'https://www.hkstockradar.com/futurehsinet.htm'
headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
}
response = requests.get(url,headers = headers)
soup = BeautifulSoup(response.text, "html.parser")
result_1 = soup.find_all('tr',attrs={'style':'height:22px; background:#F0F0F0; text-align:center; '})
result_2 = soup.find_all('tr',attrs={'style':'height:22px; background:#FFFFFF; text-align:center; '})
result = result_1 + result_2
# result = soup.find_all('tr',attrs={'style':'height:22px; background:#F0F0F0; text-align:center'})

# 收市日期	總數	增/ 減	淨數	增/ 減	開市價	最高	最低	收市價	升 / 跌	成交量	月份
for x in result:
    HSIIndex = {}
    count = 0
    for data in x.children:
        if data != '\n':
            if count == 0:
                d = (data.string).split('/')
                HSIIndex['date'] = d[0] + '/' + d[1]
                HSIIndex['timestamp'] = time.mktime(datetime.datetime.strptime(data.string, "%m/%d/%Y").timetuple())
            elif count == 1:
                HSIIndex['total'] = data.string
            elif count == 2:
                HSIIndex['total_diff'] = data.string
            elif count == 3:
                HSIIndex['pure'] = data.string
            elif count == 4:
                HSIIndex['pure_diff'] = data.string
            elif count == 5:
                HSIIndex['open'] = data.string
            elif count == 6:
                HSIIndex['hightest'] = data.string
            elif count == 7:
                HSIIndex['lowest'] = data.string
            elif count == 8:
                HSIIndex['close'] = data.string
            elif count == 9:
                HSIIndex['diff'] = data.string
            elif count == 10:
                HSIIndex['volumes'] = data.string
            elif count == 11:
                HSIIndex['month'] = data.string    
            count = count+1
    HSIIndexLists.append(HSIIndex)
    
HSIIndexLists.sort(key=operator.itemgetter('timestamp'))
# print(HSIIndex)
print(HSIIndexLists)


HSIIndexLists = [x for x in HSIIndexLists if x['total'] != ' ']

date = list(map(lambda x: x['date'],HSIIndexLists))
total = list(map(lambda x: int(x['total']),HSIIndexLists))
total_diff = list(map(lambda x: int(x['total_diff']),HSIIndexLists))
day_close = list(map(lambda x: int(x['close']),HSIIndexLists))
pure = list(map(lambda x: int(x['pure']),HSIIndexLists))
pure_diff = list(map(lambda x: int(x['pure_diff']),HSIIndexLists))

# myfont = FontProperties(fname=r'/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc')
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(15,10),dpi=100,linewidth = 2)
plt.plot(date,total,'r-',color = 'r', label="總數")
plt.plot(date,total_diff,'r-',color = 'g', label="總數 增/減")
plt.plot(date,day_close,'r-',color = 'b', label="收市價")
plt.plot(date,pure,'r-',color = 'y', label="淨數")
plt.plot(date,pure_diff,'r-',color = 'm', label="淨數 增/減")

plt.title('期指 未平倉合約',x=0.5, y=1.03)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel("2019-2020", fontsize=15, labelpad = 20)
plt.ylabel("#", fontsize=15, labelpad = 20)
plt.legend(loc = "best", fontsize=15)
plt.show()