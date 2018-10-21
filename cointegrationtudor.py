#Cointegration
import statsmodels.tsa.stattools as ts
import numpy as np
import pandas as pd
import datetime
from pandas_datareader import data, wb
import pandas_datareader as pdr
import quandl

data1 = quandl.get("WIKI/AAPL", start_date="2006-10-01", end_date="2012-01-01")

data2 = quandl.get("EOD/HD", start_date="2006-10-01", end_date="2012-01-01")

#data1['key']=data1.index

#data2['key']=data1.index

x1 = data1['Close']

y1 = data1['Close']

#result = pd.merge(data1, data1, on='key')


#x1=result['Close_x']



#y1=result['Close_y']


coin_result = ts.coint(x1, y1)
print(coin_result)
