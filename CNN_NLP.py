"""
import numpy as np
import csv, numpy

dataFile = open("./mystery_symbol_train.csv", "r")

dataReader = csv.reader(dataFile, delimiter=",")
for i in range(10):
    print(dataReader.__next__())
"""

import pickle, quandl, re, json, random
import urllib.request
from googlesearch import search
from bs4 import BeautifulSoup as bs

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, Dense, Embedding
from tensorflow.keras.optimizers import RMSprop

keywords = ["copper", "aluminium", "zinc", "lead", "gold",
            "oil", "alloy", "tin", "nickel", "cobalt", "molybdenum",
            "steel", "iron", "platinum", "palladium",
            "lme", "battery", "grade", "lithium", "electric", ]

date = [27, 6, 2016]

def getHtml(page):
    req = urllib.request.Request(
        page, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
    return urllib.request.urlopen(req).read().decode("utf-8")

def getLinksQuery(query):
    return list(search(query, stop=10))

def getText(html):
    script = bs(html, features="html.parser")
    for s in script(["script", "style"]):
        s.extract()
    return script.body.get_text().replace("\n", "  ")

def getKeyWordsDesc(desc):
    words = desc.lower().split(" ")
    words = [w for w in words if w in keywords]
    freqs = list(set(words))
    return freqs # Return key words
    
    

def formatDate(date, sep=""):
    return ("{2:04d}"+sep+"{1:02d}"+sep+"{0:02d}").format(*date)

def getNameFromTicker(ticker):
    return quandl.get_table("IFT/NSA", date="2016-06-27", ticker=ticker,
                   qopts={"columns":"name"}).name[0]

def getKaggleTitles(date):
    f = pickle.loads(open("./reuters/"+formatDate(date)+".pkl", "rb").read())
    titles = list(map(lambda x: x["title"], f))
    return titles

def getSentiment(dates, ticker=None):
    dates = [formatDate(d, "-") for d in dates] if len(dates) != 3 else formatDate(dates, "-")
    f = 1
    if not ticker:
        f = quandl.get_table("IFT/NSA",
                             date=dates,
                             paginate=True,
                             qopts={"columns":["ticker", "sentiment", "news_volume"]})
    else:
        f = quandl.get_table("IFT/NSA",
                             date=dates,
                             ticker=ticker,
                             paginate=True,
                             qopts={"columns":["ticker", "date", "sentiment", "news_volume"]})

        lst = list(zip(f.date, f.ticker, f.sentiment, f.news_volume))
        datesStr = list(set(f.date)); datesStr.sort()
        ret = [[] for i in range(len(datesStr))]
        for i in lst:
            ret[datesStr.index(i[0])].append((i[1], i[2], i[3]))
        return ret
            

def getKeywords(search, ticker=False):
    # We want to find the company name if we don't have it already
    # if ticker, make company name
    if ticker: search = getNameFromTicker(search)
    return getKeyWordsDesc(getText(getHtml(getLinksQuery(search)[0])))
        

def getAllTickers():
    return list(set(quandl.get_table("IFT/NSA", date="2016-06-27",
                   paginate=True, qopts={"columns":"ticker"}).ticker))
"""
#using_tickers = getAllTickers()
#using_tickers.shuffle()
#using_tickers = using_tickers[0:100]

x_train = [] # Want all 
y_train = []


max_features = 10000
embeddingSize= 256
maxTitleLen  = 25


#model = Sequential()
#model.add(Embedding(max_features, embeddingSize))
#model.add(Conv1D(kernel_size=(
"""
