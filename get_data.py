import json
import requests
from pyquery import PyQuery as pq
from pytrends.request import TrendReq 

class Data():

    def get_data(keyword_list, train_cities, train_scores):
        pt = TrendReq()
        
        stats = {}
        f = open('cities.txt', 'r')
        text = f.readlines()[0]
        cities = text[1:-1].replace('\'', '').split(',')
        f.close()
        keyword_map = {}        
        train_stats = {}
        for i in range(len(keyword_list)):
            keyword_map[keyword_list[i]] = i
        for city in cities:
            stats[city] = [0]*(len(keyword_list)+1)
        for word in keyword_list:
            
            pt.build_payload(kw_list=[word])
            data = pt.interest_by_region(resolution = 'CITY').T
            min_score = 100
            for city in cities:
                
                if city in data.keys():
                    score = int(data.get(city).get(0))
                    stats[city][keyword_map[word]] = score
                    if score < min_score:
                        min_score = score
                
            for city in cities:
                if not city in data.keys():
                    stats[city][keyword_map[word]] = max(min_score-1, 0)
                    
        for i in range(len(train_cities)):
            stats[train_cities[i]][len(keyword_list)] = train_scores[i]
            train_stats[train_cities[i]] = stats[train_cities[i]].copy()
            del stats[train_cities[i]]
        
        return stats, train_stats







