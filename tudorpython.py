""" Python for Finance Tutorial:
Pandas package: pandas_datareader package allows for reading in data sources
"""

#Sample stock data collection using pandas

import pandas_datareader as pdr
import datetime
aapl = pdr.get_data_yahoo('AAPL',
                          start=datetime.datetime(2006, 10, 1),
                          end=datetime.datetime(2012, 1, 1))

#Stock data collection using quandl

import quandl
aapl = quandl.get("WIKI/AAPL", start_date="2006-10-01", end_date="2012-01-01")

"""Working with Time series data

Useful commands for handling time-series data:"""

aapl.head() #first rows
aapl.tail() #last rows
aapl.describe() #getting some description

"""Extra columns:

Volume: register the number of shares that got traded during a single day
Adj Close: closing price on the day"""

#To save data to a csv file

import pandas as pd
aapl.to_csv('data/aapl_ohlc.csv') #folder/nameoffile
df = pd.read_csv('data/aapl_ohlc.csv', header=0, index_col='Date', parse_dates=True)

# More useful commands

aapl.index #finding index
aapl.columns #inspect columns
variable = aapl['Columnname'][indexing] #where indexing = -10:, 2:, :3 etc.
type(variable) #to check type of a variable


#Location functions

# Inspect the first rows of November-December 2006
print(aapl.loc[pd.Timestamp('2006-11-01'):pd.Timestamp('2006-12-31')].______)

# Inspect the first rows of 2007
print(aapl.loc['2007'].______)

# Inspect November 2006
print(aapl.____[22:43])

# Inspect the 'Open' and 'Close' values at 2006-11-01 and 2006-12-01
print(aapl.iloc[[22,43], [0, 3]])

"""Sampling and resampling""""

# Sample 20 rows
sample = aapl.sample(20)

# Print `sample`
print(sample)

# Resample to monthly level
monthly_aapl = aapl.resample('M').mean()

# Print `monthly_aapl`
print(monthly_aapl)

"""Adding columns and data to the dataset"""

# Add a column `diff` to `aapl`
aapl['diff'] = aapl.Open - aapl.Close

# Delete the new `diff` column
del aapl['diff']  #needs to be commented if you want not to delete all data


"""VISUALIZING TIME SERIES DATA""""

import matplotlib.pyplot as plt

# Plot the closing prices for `aapl`
aapl['Close'].plot(grid=True)

# Show the plot
plt.show()

"""COMMON FINANCIAL ANALYSIS"""

# RETURNS

#Simple daily percentage change, no dividends etc


import numpy as np

# Import `numpy` as `np`
import numpy as np

# Assign `Adj Close` to `daily_close`
daily_close = aapl[['Adj Close']]

# Daily returns
daily_pct_change = daily_close.pct_change()   ##KEY COMMAND

# Replace NA values with 0
daily_pct_change.fillna(0, inplace=True)

# Inspect daily returns
print(daily_pct_change)

# Daily log returns
daily_log_returns = np.log(daily_close.pct_change()+1)

# Print daily log returns
print(daily_log_returns)

################### Quarterly returns, use Resample

# Resample `aapl` to business months, take last observation as value
monthly = aapl.resample('BM').apply(lambda x: x[-1])

# Calculate the monthly percentage change
monthly.pct_change()

# Resample `aapl` to quarters, take the mean as value per quarter
quarter = aapl.resample("4M").mean()

# Calculate the quarterly percentage change
quarter.pct_change()

# daily log RETURNS

daily_log_returns_shift = np.log(daily_close /daily_close_shift(1))

"""Plotting Histogram of data""""


# Plot the distribution of `daily_pct_c`
daily_pct_change.hist(bins=50)

# Show the plot
plt.show()

# Pull up summary statistics
print(daily_pct_change.describe())

"""Cumulative daily rate of return"""

# Calculate the cumulative daily returns
cum_daily_return = (1 + daily_pct_change).cumprod()

# Print `cum_daily_return`
print(cum_daily_return)

""""Function for getting tickers"""


def get(tickers, startdate, enddate):
  def data(ticker):
    return (pdr.get_data_yahoo(ticker, start=startdate, end=enddate))
  datas = map (data, tickers)
  return(pd.concat(datas, keys=tickers, names=['Ticker', 'Date']))

tickers = ['AAPL', 'MSFT', 'IBM', 'GOOG']
all_data = get(tickers, datetime.datetime(2006, 10, 1), datetime.datetime(2012, 1, 1))

#More financial data on
# https://www.datacamp.com/community/tutorials/finance-python-trading


""" MOVING WINDOWS

Moving windows are there when you compute the statistic on a
window of data represented by a particular period of time and
then slide the window across the data by a specified interval.
That way, the statistic is continually calculated as long as
the window falls first within the dates of the time series.

# Basically a moving average - loads of different options on

http://pandas.pydata.org/pandas-docs/version/0.17.0/api.html#standard-moving-window-functions

Example code:                                           """

# Isolate the adjusted closing prices
adj_close_px = aapl['Adj Close']

# Calculate the moving average
moving_avg = adj_close_px.rolling(window=40).mean()

# Inspect the result
print(moving_avg[-10:])

"""Volatility Calculation:
The volatility of a stock is a measurement of the change in variance
in the returns of a stock over a specific period of time. It is common
to compare the volatility of a stock with another stock to get a feel
for which may have less risk or to a market index to examine the stock’s
volatility in the overall market. Generally, the higher the volatility,
the riskier the investment in that stock, which results in investing
in one over another.

"""

# Define the minumum of periods to consider
min_periods = 75

# Calculate the volatility
vol = daily_pct_change.rolling(min_periods).std() * np.sqrt(min_periods)

# Plot the volatility
vol.plot(figsize=(10, 8))

# Show the plot
plt.show()

""" Ordinary Least-Squares Regression (OLS)

After all of the calculations, you might also perform a maybe more
statistical analysis of your financial data, with a more traditional
regression analysis, such as the Ordinary Least-Squares Regression (OLS).

To do this, you have to make use of the statsmodels library, which not
only provides you with the classes and functions to estimate many
different statistical models but also allows you to conduct statistical
 tests and perform statistical data exploration.

Note that you could indeed to the OLS regression with Pandas, but that
the ols module is now deprecated and will be removed in future versions.
It is therefore wise to use the statsmodels package."""


# Import the `api` model of `statsmodels` under alias `sm`
import statsmodels.api as sm

# Import the `datetools` module from `pandas`
from pandas.core import datetools

# Isolate the adjusted closing price
all_adj_close = all_data[['Adj Close']]

# Calculate the returns
all_returns = np.log(all_adj_close / all_adj_close.shift(1))

# Isolate the AAPL returns
aapl_returns = all_returns.iloc[all_returns.index.get_level_values('Ticker') == 'AAPL']
aapl_returns.index = aapl_returns.index.droplevel('Ticker')

# Isolate the MSFT returns
msft_returns = all_returns.iloc[all_returns.index.get_level_values('Ticker') == 'MSFT']
msft_returns.index = msft_returns.index.droplevel('Ticker')

# Build up a new DataFrame with AAPL and MSFT returns
return_data = pd.concat([aapl_returns, msft_returns], axis=1)[1:]
return_data.columns = ['AAPL', 'MSFT']

# Add a constant
X = sm.add_constant(return_data['AAPL'])

# Construct the model
model = sm.OLS(return_data['MSFT'],X).fit()

# Print the summary
print(model.summary())

"""
                            OLS Regression Results
==============================================================================
Dep. Variable:                   MSFT   R-squared:                       0.280
Model:                            OLS   Adj. R-squared:                  0.280
Method:                 Least Squares   F-statistic:                     514.2
Date:                Sat, 20 Oct 2018   Prob (F-statistic):           2.07e-96
Time:                        21:18:17   Log-Likelihood:                 3513.2
No. Observations:                1322   AIC:                            -7022.
Df Residuals:                    1320   BIC:                            -7012.
Df Model:                           1
Covariance Type:            nonrobust
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
const         -0.0006      0.000     -1.287      0.198      -0.002       0.000
AAPL           0.4404      0.019     22.677      0.000       0.402       0.479
==============================================================================
Omnibus:                      267.360   Durbin-Watson:                   2.071
Prob(Omnibus):                  0.000   Jarque-Bera (JB):             6987.230
Skew:                          -0.202   Prob(JB):                         0.00
Kurtosis:                      14.255   Cond. No.                         41.6
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is
correctly specified.

IMPORTANT:        &&&&&&&&&&&&&&     .info() FUNCTION WORKS &&&&&&&&&&&&&&&&&&

"""

#PLOT OF LEAST SQUARES Regression

# Import matplotlib
import matplotlib.pyplot as plt

# Plot returns of AAPL and MSFT
plt.plot(return_data['AAPL'], return_data['MSFT'], 'r.')

# Add an axis to the plot
ax = plt.axis()

# Initialize `x`
x = np.linspace(ax[0], ax[1] + 0.01)

# Plot the regression line
plt.plot(x, model.params[0] + model.params[1] * x, 'b', lw=2)

# Customize the plot
plt.grid(True)
plt.axis('tight')
plt.xlabel('Apple Returns')
plt.ylabel('Microsoft returns')

# Show the plot
plt.show()



###########################################################################


#Plot of rolling correltion:

# Import matplotlib
import matplotlib.pyplot as plt

# Plot the rolling correlation
return_data['MSFT'].rolling(window=252).corr(return_data['AAPL']).plot()

# Show the plot
plt.show()
