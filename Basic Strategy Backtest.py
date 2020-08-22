# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 20:57:08 2020

@author: sayuj
"""

""" RUN THIS SECTION FIRST AND ONLY ONCE """

import pandas as pd
import pandas_datareader.data as web

import matplotlib.pyplot as plt

from datetime import datetime

from dotenv import load_dotenv

today = datetime.strftime(datetime.today(), "%Y-%m-%d")

# Adjust the dates to whatever dates you want to start and end the backtest
BEGIN_DATE = '2009-12-31'
END_DATE = today

# Load the API key from a .env file
load_dotenv()

# The following function extracts stock data from a specific data source
# (CSV, API, JSON, etc.)
def get_symbols(symbols, data_source, begin_date, end_date=today):
    
    """
    Parameters
    ----------
    symbols : stock ticker you want to pull data for
    data_source : data source that the stock data will be pulled from (CSV, API, JSON, etc.)
    begin_date : start of lookback period/start point for the timeframe you want data for (default is None)
    end_date : end of lookback period/end point for the timeframe you want data for (default is None)

    Returns
    -------
    A dataframe of stock data for the specified ticker that includes opening, high, low, and closing price, as well as stock volume
    """
    
    out = []
    for symbol in symbols:
        df = web.DataReader(symbol, data_source, begin_date, end_date, api_key=os.getenv('API_KEY'))\
        [['AdjOpen','AdjHigh','AdjLow','AdjClose','AdjVolume']].reset_index()
        df.columns = ['Date','Open','High','Low',symbol,'Volume']
        df = df[::-1].reset_index()
        out.append(df.sort_index())
    return out

data = pd.read_csv('sp500tickers.csv', engine='python')
sp500 = {}

# The following may take a few minutes due to the large list of stock data that must be loaded
for symbol in data.Symbol:
    try:
        df = get_symbols([symbol], 'quandl',
                        BEGIN_DATE, END_DATE)
        sp500[symbol] = df
        print(symbol, 'Loaded')
    except:
        print(f'An error occured getting the symbol for {symbol}')
        continue

#%%

# Set how many days you want to conduct the backtest for
LOOKBACK_PERIOD = 10

cost = {}
buy = []
sell = []
holdings = set()

# The following function uses the database of stock data loaded above to implement a given trading strategy and report the backtest results
# The strategy involved buying a stock if the current day's opening price is greater than the previous day's closing price and selling if vice versa
def strategy(days, symbols):
    
    """
    Parameters
    ----------
    days : lookback period in days that the user would like to backtest for
    symbols: a dictionary of stock tickers and pricing data
    
    Returns
    -------
    The shares of stock that were bought and sold each day, as well as all
    shares currently being held in the portfolio. Up-to-date profit and loss
    is also reported each day. A graph outlining overall profitability of the
    strategy is generated at the very end of the backtest.
    """
    
    total_profits = []
    for day in range(days):
        
        PnL = 0
        
        print('Day {}'.format(day))
        for symbol in symbols:
            open_price = symbols.get(symbol)[0].iloc[day]['Open']
            close_price = symbols.get(symbol)[0].iloc[day-1][symbol]

            if open_price > close_price and symbol not in holdings:
                buy.append(symbol)
                holdings.add(symbol)
                cost[symbol] = open_price

            elif open_price < close_price and symbol in holdings:
                sell.append(symbol)
                holdings.remove(symbol)
                profit = open_price - cost.get(symbol)
                PnL += profit

        print('Current Holdings: ', holdings)
        print('Bought: ', buy)
        print('Sold: ', sell)
        print('PnL: ', PnL)
        total_profits.append(PnL)
    
    plt.figure(figsize=(14, 5), dpi=100)
    plt.plot(range(0, days), total_profits)
    plt.xlabel('Day')
    plt.ylabel('PnL')
    plt.title('Portfolio Profit and Loss')
    plt.legend()
    plt.show()
    
strategy(LOOKBACK_PERIOD, sp500)
