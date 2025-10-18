import warnings
import requests
import config
import yfinance as yf
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
        with open(HISTORY_FILE, "a") as f:
            f.write(f"{date} ({abbreviated_weekday}): ${equity:.2f}\n")

    def fill_list(self):
        self.stockList = self.quick_fill()
        print("stock list found:")
        for item in self.stockList:
            print(f"Item: {item}")

    def quick_fill(self):
        tickers = self.symbolBot.stocks_full_list()
        return tickers

    def fill_stock_data_from_yfinance(self, tickers):
        today = datetime.now()
        lastWeek = today - timedelta(7)
        results = []

        # === Pull all history at once ===
        all_history = yf.download(tickers, group_by='ticker', threads=True)

        for ticker in all_history:
            try:
                results.append(all_history[ticker].tail())

            except Exception as e:
                print(f"Error retrieving data for {ticker}: {e}")
                continue

        self.stockList = results
        # return results
    
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
            print(f"length of most_actives: {len(most_actives)}")

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

    def populate_stockList(self, stocks):
        try:
            for stock in stocks:
                try:
                    '''
                    #The following three lines is one of the ways to get info from alpaca
                    req = StockLatestQuoteRequest(symbol_or_symbols=stock['symbol'])
                    latest_trade = dataClient.get_stock_latest_trade(req)[stock['symbol']]
                    latest_price_alpaca = latest_trade.price
                    '''
                    #print(f"stock['symbol']: {stock['symbol']}")
                    ticker = yf.Ticker(stock['symbol'])
                    fast_info = ticker.fast_info

                    '''
                    # These contain more info but are generally considered too dense
                    info = ticker.info
                    cash_flow = ticker.cash_flow
                    income_statement = ticker.income_stmt
                    financials = ticker.financials
                    growth_estimates = ticker.growth_estimates
                    ''' 

                    last_price = float(fast_info.get('lastPrice', 0))
                    previous_close = fast_info.get('previousClose', 0)
                    percent_change = 0
                    if previous_close:
                        percent_change = ((last_price - previous_close) / previous_close) * 100
                    percent_change = self.format_number(percent_change)


                    open = fast_info.get('open', 0)
                    price_target = ticker.analyst_price_targets.get('current', 0)
                    year_low = fast_info.get('yearLow', 0)
                    year_high = fast_info.get('yearHigh', 0)
                    fifty_day_average = fast_info.get('fiftyDayAverage', 0)
                    two_hundred_day_average = fast_info.get('twoHundredDayAverage', 0)
                    ten_day_volume = fast_info.get('tenDayAverageVolume', 0)
                    three_month_volume = fast_info.get('threeMonthAverageVolume', 0)
                    balance_sheet = ticker.balance_sheet if ticker.balance_sheet is not None else "n/a"
                    stock['other_info'] = ({
                        "symbol": stock['symbol'],
                        "last_price": self.format_number(last_price),
                        "open": self.format_number(open),
                        "analyst_price_target": self.format_number(price_target),
                        "year_low": self.format_number(year_low),
                        "year_high":self.format_number(year_high),
                        "fifty_day_average": self.format_number(fifty_day_average),
                        "two_hundred_day_average": self.format_number(two_hundred_day_average),
                        "ten_day_volume": self.format_number(ten_day_volume),
                        "three_month_volume": self.format_number(three_month_volume),
                        "balance_sheet": balance_sheet
                          })
                    if 'price' not in stock:
                        stock['price'] = last_price
                    if 'percent_change' not in stock:
                        stock['percent_change'] = percent_change

                except Exception as e:
                    print(f"Error in populate_stockList() for symbol: {stock['symbol']}: {e}")

        except Exception as e:
            print("Error in populate_stockList(): {e}")

        return stocks
