import warnings
import requests
import config
import os
import yfinance as yf
from time import sleep
from auth.connectClient import dataClient, liveTradingClient
from alpaca.data.requests import StockLatestQuoteRequest
from data.symbolBot import SymbolBot
from datetime import datetime, timedelta


warnings.simplefilter(action='ignore', category=UserWarning)

class StockBot:

    def __init__(self):
        self.symbolBot = SymbolBot()
        self.stockList = []
        self.movers = []
        self.CheapUpTrenders =[]
        self.CheapDownTrenders = []
        self.ExpensiveUpTrenders =[]
        self.ExpensiveDownTrenders = []
        pass
    
    def add_equity_to_history(self):
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        abbreviated_weekday = now.strftime('%a')
        HISTORY_FILE = "equity_history.txt"

        live_account = liveTradingClient.get_account()
        equity = float(live_account.equity)

        # Get previous equity if available
        last_equity = None
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                lines = f.readlines()
                if lines:
                    last_line = lines[-1].strip()
                    try:
                        # extract last recorded value, assuming format: YYYY-MM-DD (Mon): $12345.67
                        last_equity = float(last_line.split('$')[-1])
                    except (IndexError, ValueError):
                        last_equity = None

        # Calculate percent change if possible
        if last_equity and last_equity > 0:
            pct_change = ((equity - last_equity) / last_equity) * 100
            entry = f"{date} ({abbreviated_weekday}):({pct_change:+.2f}%) ${equity:.2f}\n"
        else:
            entry = f"{date} ({abbreviated_weekday}): ${equity:.2f}\n"

        # Append entry to file
        with open(HISTORY_FILE, "a") as f:
            f.write(entry)

    def getMovers(self, max_price=20, min_price=.10):
        #print("Inside getMovers()")

        headers = {"accept": "application/json",
                   "APCA-API-KEY-ID": config.ALPACA_API_KEY,
                   "APCA-API-SECRET-KEY": config.ALPACA_SECRET_KEY}
        try:
            url = "https://data.alpaca.markets/v1beta1/screener/stocks/movers?top=50"
            response = requests.get(url, headers=headers)
            # print(response.text)
            data = response.json()
            '''
            for item in response:
                print(item)
            '''
            for mover_type in ["gainers", "losers"]:
                # print(f"\n---{mover_type.upper()} ---")
                for item in data.get(mover_type,[]):
                    # print(f"Symbol: {item['symbol']}, Price: {item['price']}, Change: {item['percent_change']}%")
                    price = item.get('price', 0) or 0
                    if(min_price < price < max_price): 
                        self.movers.append(item)
                        self.stockList.append(item)
                        if item not in self.stockList: self.stockList.append(item)
        except (requests.RequestException, ValueError, KeyError) as e:
            print(f"Error fetching movers: {e}")

    def getMostActiveVolume(self, max_price=20, min_price=.10):
        headers = {"accept": "application/json",
                   "APCA-API-KEY-ID": config.ALPACA_API_KEY,
                   "APCA-API-SECRET-KEY": config.ALPACA_SECRET_KEY}
        try:
            url2 = "https://data.alpaca.markets/v1beta1/screener/stocks/most-actives?top=100"
            response2 = requests.get(url2, headers=headers)
            active_data = response2.json()
            most_actives = active_data.get('most_actives', active_data) if isinstance(active_data, dict) else active_data

            existing = []
            for stock in self.stockList:
                existing.append(stock['symbol'])
                
                
            for item in most_actives:
                symbol = item.get('symbol')
                #if symbol not in existing_symbols : self.movers.append(item)
                if symbol not in existing: self.stockList.append({'symbol':symbol})
            
        except (requests.RequestException, ValueError, KeyError) as e:
            print(f"Error fetching most actives: {e}")
    
    def format_number(self, value):
        if value is None:
            return "N/A"
        try:
            if value >= 1_000_000_000:
                return f"{value / 1_000_000_000:.2f}B"
            if value >= 1_000_000:
                return f"{value / 1_000_000:.2f}M"
            return f"{float(value):,.2f}"
        except (ValueError, TypeError):
            return str(value) #return as string if not a valid number

    def grab_snapshots(self, stocks):
        filtered = []
        for stock in stocks:
            filtered.append({
                'symbol': stock['symbol'], 
                'price': stock['price'], 
                'percent_change': stock['percent_change'], 
                'market_cap': stock['market_cap'], 
                'volume': stock['volume'], 
                'ten_day_volume': stock['ten_day_volume'], 
                'three_month_volume': stock['three_month_volume'],  
                'shares': stock['shares'], 
                'float_shares': stock['float_shares'],
                'shares_outsanding': stock['shares_outstanding'],
                'price_to_earnings': stock['price_to_earnings'],
                'price_to_book': stock['price_to_book'],
                'price_to_sales': stock['price_to_sales'],
                'float_rotation': stock['float_rotation'],
                'fifty_day_average': stock['fifty_day_average'],
                'two_hundred_day_average': stock['two_hundred_day_average'],
                'year_low' : stock['year_low'],
                'price_target': stock['price_target'],
                'earnings_date': stock['earnings_date'],
                'news': stock['news']
                #'balance_sheet': stock['balance_sheet']
            })

        return filtered