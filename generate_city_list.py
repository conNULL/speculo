import json
import requests
from pyquery import PyQuery as pq
from pytrends.request import TrendReq 

pt = TrendReq()

keyword_list = ['tech', 'apple', 'phone', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'dog', 'cat']
train_cities = ['Toronto', 'San Francisco', 'Boston']
stats = {}
all_cities = set([])
for word in keyword_list:
    word_stats =[]
    pt.build_payload(kw_list=[word])
    data = pt.interest_by_region(resolution = 'CITY').T
    for city in data.keys():
        all_cities.add(city)
        word_stats.append(data.get(city).get(0))
    stats[word] = word_stats
    
c = list(all_cities)
c.sort()
f = open('cities.txt', 'w', encoding='utf-8')
f.write('[')
for city in c:
    f.write('\'' + city + '\',')
f.write(']')
f.close()





