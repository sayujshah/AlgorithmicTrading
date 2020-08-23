# Algorithmic Trading

## About the Project

Algorithmic trading is a growing field for investors who are looking to take advantage of the power of big data and AI in order to improve their trading strategy. I am attempting to creat my own small-scale algorthmic trading platform for personal use. The platform should include the following features:
* Loading/Handling stock data
* Technical analysis
* Sentiment analysis
* Machine learning/Deep learning
* And more!

The platform will sift through a database of stocks and purchase those that meet a pre-defined criteria/set of rules and sell those that do not. The platform would execute trades on the user's behalf, however it will be a white box (at least at first) so the user knows exactly what the machine is doing and can make any adjustments as needed.

Before I develop my platform, I will be documenting my learning process here. However, when I have built up the skills and knowledge to develop my own strategy, I will not be sharing the final script as it will render the program useless. Rather, I will share a framework for others to build their own strategy from.

# Current Projects

## Basic Strategy Backtest

For my first mini-project to develop my skills, I have created a small program that backtests a simple strategy of buying a stock when the current day's opening price is greater than the previous day's closing price and selling when vice versa. The program will backtest for a user-specified number of days over a list of stocks (see the "sp500tickers.csv" file for a list of all the S&P 500 tickers). At the end of each day, the program will alert the user of what was bought, sold, what stocks are currently in the portfolio, and profit and loss to date. At the end of the backtest, a chart of the profit and loss is graphed to depict how successful the strategy was.

NOTE: The first cell should be run first and only needs to be run once. It takes a couple of minutes since all the stocks from the S&P 500 are being loaded into a dictionary. You may then run the second cell as many times as you would like. There will be no need to run the first cell again since all data will be stored locally at that point.
