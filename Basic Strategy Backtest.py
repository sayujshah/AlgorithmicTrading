# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 20:57:08 2020

@author: sayuj
"""

import pandas as pd
import pandas_datareader.data as web

import numpy as np

import matplotlib.pyplot as plt

from datetime import datetime

import os

# API key is being pulled from a seperate config.py file
import config

today = datetime.strftime(datetime.today(), "%Y-%m-%d")

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
        df = web.DataReader(symbol, data_source, begin_date, end_date, api_key=config.api_key)\
        [['AdjOpen','AdjHigh','AdjLow','AdjClose','AdjVolume']].reset_index()
        df.columns = ['Date','Open','High','Low',symbol,'Volume']
        df = df[::-1].reset_index()
        out.append(df.sort_index())
    return out

symbol_path = """ INSERT YOUR PATH HERE """
symbol_list = os.listdir(symbol_path) # It is recommended that this list is shortened at first in order to speed up testing

symbols = []
for i in symbol_list:
    symbol = i.replace('.csv','')
    symbols.append(symbol)

#%%

buy = []
sell = []
holdings = []
profit_list = []
total_profit = []

def strategy():

    """
    This function sifts through a database of stocks and pulls historical
    price data. It then implements a trading strategy of buying if the opening
    price is greater than the previous day's closing price and sell if vice
    versa. This strategy is checked daily. The user may indicate how many days
    back they would like to backtest.
    """
    
    day = 1
    while day <= 10: # This is a placeholder for testing purposes only. The value would be much larger depending on how many days one wants to backtest for
        print('Day {}'.format(day))
        for i in symbols:
            try:
                df = get_symbols([i],data_source='quandl',\
                                         begin_date='2009-12-31', end_date=today)
                # print('{} Loaded'.format(i))
                open_price = df[0].iloc[day]['Open']
                close_price = df[0].iloc[day - 1][i]
                
                if open_price > close_price:
                    if i not in holdings:
                        buy.append(i)
                        holdings.append(i)
                        cost = open_price
                    
                elif open_price < close_price:
                    if i in holdings:
                        sell.append(i)
                        holdings.remove(i)
                        profit = open_price - cost
                        profit_list.append(profit)
                
            except:
                pass
            
        print('Current Holdings: ', holdings)
        print('Bought: ', buy)
        print('Sold: ', sell)
        
        PnL = sum(profit_list)
        print('PnL: ', PnL)
        total_profit.append(PnL)
        
        buy.clear()
        sell.clear()

        day += 1

    plt.figure(figsize=(14, 5), dpi=100)
    plt.plot(range(1,day), total_profit)
    plt.xlabel('Day')
    plt.ylabel('PnL')
    plt.legend()
    plt.show()

# The following initiates the program
strategy()