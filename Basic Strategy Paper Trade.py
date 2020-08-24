#%%
import requests
import json
import pandas as pd
import alpaca_trade_api as tradeapi
from datetime import datetime
from dotenv import load_dotenv
import os

# Load the API key from a .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

# The following are the URLs and parameters being used to access the Alpaca API
BASE_URL = 'https://paper-api.alpaca.markets'
ACCOUNT_URL = '{}/v2/account'.format(BASE_URL)
ORDERS_URL = '{}/v2/orders'.format(BASE_URL)
QUOTE_URL = '{}/v1/last_quote/stocks/'.format(BASE_URL)
BARS_URL = '{}/v1/bars/'.format(BASE_URL)
POSITIONS_URL = '{}/v2/positions'.format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}

# The following sets the API parameters
api = tradeapi.REST(
    key_id=API_KEY,
    secret_key=SECRET_KEY,
    base_url=BASE_URL
)

#%%

today = datetime.strftime(datetime.today(), "%Y-%m-%d")

def get_account():

    """
    This function pulls account information from the Alpaca API
    and stores it in a json file
    """

    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    
    return json.loads(r.content)

def create_order(symbol, qty, side, type, time_in_force):
    
    """
    This function executes an order based on user specifications
    and returns a json file depicting the order summary
    """

    data = {
        'symbol': symbol,
        'qty': qty,
        'side': side,
        'type': type,
        'time_in_force': time_in_force
    }
    
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    
    return json.loads(r.content)

data = pd.read_csv('sp500tickers.csv', engine='python')

def get_positions():

    """
    This function pulls the current open positions in the user's Alpaca
    trading account and stores the information in a json file
    """

    r = requests.get(POSITIONS_URL, headers=HEADERS)
    
    return json.loads(r.content)

positions = get_positions()
holdings = []

for position in positions:
    holdings.append(position['symbol'])

# The following for loop executes the strategy of buying a stock if the current day's
# opening price is greater than the previous day's closing price and sells if vice versa
for symbol in data.Symbol:
    time = today+'T'+'08:31:00-05:00'
    try:
        previous_barset = api.get_barset(symbol, 'day', limit=2)
        today_barset = api.get_barset(symbol, 'day', limit=1, start=time)
        
        previous_symbol_bars = previous_barset[symbol]
        today_symbol_bars = today_barset[symbol]
        previous_close = previous_symbol_bars[0].c
        open_price = today_symbol_bars[0].o
    except:
        pass

    if open_price > previous_close and symbol not in holdings:
        create_order(symbol, 1, 'buy', 'market', 'gtc')
        print('Bought: ', symbol)
    elif open_price < previous_close and symbol in holdings:
        create_order(symbol, 1, 'sell', 'market', 'gtc')
        print('Sold: ', symbol)

#%%

def get_orders():

    """
    This function pulls information about any current open orders the user may have
    and store it in a json file
    """

    r = requests.get(ORDERS_URL, headers=HEADERS)

    return json.loads(r.content)

orders = get_orders()

print(positions)
