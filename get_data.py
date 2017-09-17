import json
import requests
from pyquery import PyQuery as pq
from pytrends.request import TrendReq 

class Data():

    def get_data(words):
        pt = TrendReq()
        
        keyword_list = ['tech','phone', 'computer']
        train_cities = ['Toronto', 'San Francisco', 'Boston']
        stats = {}
        f = open('cities.txt', 'r')
        text = f.readlines()[0]
        cities = text[1:-1].replace('\'', '').split(',')
        f.close()
        city_map = {}
        for i in range(len(cities)):
            city_map[cities[i]] = i
            
        for word in keyword_list:
            word_stats =[0]*len(cities)
            pt.build_payload(kw_list=[word])
            data = pt.interest_by_region(resolution = 'CITY').T
            min_score = 100
            for city in cities:
                
                if city in data.keys():
                    score = int(data.get(city).get(0))
                    word_stats[city_map[city]] = score
                    if score < min_score:
                        min_score = score
                
            for city in cities:
                if not city in data.keys():
                    word_stats[city_map[city]] = max(min_score-1, 0)
                    
            stats[word] = word_stats
        return stats







