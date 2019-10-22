#Cointegration for Leon

import statsmodels.tsa.stattools as ts
import numpy as np
import pandas as pd
import datetime
from pandas_datareader import data, wb
import pandas_datareader as pdr
import quandl

#data = pd.read_csv("Book1.csv")
#x1 = data['7679.5']
#x2 = data['2034']
#x3 = data['1849.00']
#x4 = data['2015']

aapl = quandl.get("WIKI/AAPL", start_date="1990-10-01", end_date="2018-01-01")
ba = quandl.get("WIKI/BA", start_date="1990-10-01", end_date="2017-12-28")

x1 = aapl['Open']
x2 = aapl['Close']

x3 = ba['Open']
x4 = ba['Close']

#result = ts.coint()
#print(result)
