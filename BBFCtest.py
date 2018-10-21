# Big Black Full Cock Test

from pandas import Series
import pandas as pd
from statsmodels.tsa.stattools import adfuller


series = Series.from_csv('dailytotalfemalebirths.csv', header=0)

X = series.values

result = adfuller(X)

print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')

for key, value in result[4].items():
 print('\t%s: %.3f' % (key, value))
