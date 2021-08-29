#!/usr/bin/env python
# coding: utf-8

# In[15]:


import requests
from bs4 import BeautifulSoup as BS
import json
import threading

import redis

import pymongo as mongo
client = mongo.MongoClient("mongodb://127.0.0.1:27017")


r = redis.Redis(host = "localhost", port = 6379 , decode_responses=True)




DBA = client["BITCOIN"]

## Make new collections

col_transactions = DBA["transactions"] 




def scraper():
    threading.Timer(30.0, scraper).start()
    url = "https://www.blockchain.com/btc/unconfirmed-transactions"
    request = requests.get(url)
    output_text = request.text
    soup = BS(request.text,features="html.parser")
    hash = soup.find_all("div", class_='sc-6nt7oh-0 PtIAf')
    names = [hash.text for hash in hash]
    hashes = names[0::4]
    times = names[1::4]
    BTC = names[2::4]
    USD = names[3::4]
    goat = max(BTC)
    index = BTC.index(goat)
    output = [hashes[index],times[index],BTC[index],USD[index]]
    
    y = {'hash': hashes[index],
        'time': times[index],
        'BTC': BTC[index],
        'USD': USD[index]
    }
    
    print(y)
    print("SCRAPER OK")
    print()
    # data

    r.set("BITCOIN",json.dumps(y))
    
    element  = r.get("BITCOIN")
    
    print(element)
    print("REDIS OK")
    print()
    
    
    load = json.loads(element)
    x = col_transactions.insert_one(load)
    ## print
    print(x.inserted_id) 
    print("MONGO OK")

scraper()
# In[ ]:




