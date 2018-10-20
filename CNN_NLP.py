"""from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, Dense
from tensorflow.keras.optimizers import RMSprop

import numpy as np
import csv, numpy

dataFile = open("./mystery_symbol_train.csv", "r")

dataReader = csv.reader(dataFile, delimiter=",")
for i in range(10):
    print(dataReader.__next__())
"""

import pickle, quandl

date = [27, 6, 2016]

def formatDate(date, sep=""):
    return ("{2:04d}"+sep+"{1:02d}"+sep+"{0:02d}").format(*date)

def getNameFromTicker(ticker):
    return quandl.get_table("IFT/NSA", date="2016-06-27", ticker=ticker,
                   qopts={"columns":"name"}).name[0]

def getKaggleTitles(date):
    f = pickle.loads(open("./reuters/"+formatDate(date)+".pkl", "rb").read())
    titles = list(map(lambda x: x["title"], f))
    return titles

def getSentiment(date):
    f = quandl.get_table("IFT/NSA",
                         date=formatDate(date, "-"),
                         paginate=True,
                         qopts={"columns":["ticker", "sentiment", "news_volume"]})
    return list(zip(f.ticker, f.sentiment, f.news_volume))
        

getKaggleTitles(date)
