import requests
import config
import yfinance as yf
from data.symbolBot import SymbolBot
from datetime import datetime, timedelta

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
                # print(f"{all_history[ticker]}")
                '''
                # yfinance returns different formats if 1 ticker vs many
                if len(tickers) > 1:
                    history = all_history[ticker]
                else:
                    history = all_history

                if history.empty:
                    continue

                latestVolume = int(history['Volume'].iloc[-1] or 0)

                if len(history) >= 2:
                    prevClose = round(history['Close'].iloc[-2], 2)
                    latestClose = round(history['Close'].iloc[-1], 2)
                    priceChangePercentage = round(((latestClose - prevClose) / prevClose) * 100, 2)
                else:
                    prevClose = 0
                    latestClose = 0
                    priceChangePercentage = 0

                # Still need individual calls for shares (no batch method for this in yfinance)
                shares_df = yf.Ticker(ticker).get_shares_full(start=lastWeek, end=today)
                if shares_df is None or shares_df.empty:
                    print(f"No share count data for {ticker}")
                    continue

                shareCount = int(shares_df.iloc[-1] or 0)
                if shareCount == 0:
                    print(f"Share count is 0 for {ticker}")
                    continue

                volumeChange = round(float((latestVolume / shareCount) * 100), 2)

                results.append({
                    'ticker': ticker,
                    'volume': latestVolume,
                    # 'shares': shareCount,
                    # 'volumeChange': volumeChange,
                    'prevClose': prevClose,
                    'latestClose': latestClose,
                    'priceChangePercentage': priceChangePercentage
                })
                '''
                results.append(all_history[ticker].tail())

            except Exception as e:
                print(f"Error retrieving data for {ticker}: {e}")
                continue

        self.stockList = results
        # return results
    
    def getMovers(self, max_price=20, min_price=.10):
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
                    if(min_price < price < max_price): self.movers.append(item)
        except (requests.RequestException, ValueError, KeyError) as e:
            print(f"Error fetching movers: {e}")

        '''
        try:
            existing_symbols = {m['symbol'] for m in self.movers}
            url2 = "https://data.alpaca.markets/v1beta1/screener/stocks/most-actives?top=100"
            response2 = requests.get(url2, headers=headers)
            active_data = response2.json()
            most_actives = active_data.get('most_actives', active_data) if isinstance(active_data, dict) else active_data
            print(f"length of most_actives: {len(most_actives)}")

            for item in most_actives:
                symbol = item.get('symbol')
                price = item.get('price', 0)
                if symbol not in existing_symbols : self.movers.append(item)
        except (requests.RequestException, ValueError, KeyError) as e:
            print(f"Error fetching most actives: {e}")
        '''


    def listStocks(self, list=["empty List.."], limit = 200):
        index = 0
        for stock in list:
            if(index == limit): break
            index += 1

            symbol = stock['symbol']
            price = self.format_number(stock['price'])
            percent_change = self.format_number(stock['percent_change'])

            if 'pb_ratio' in stock:
                pb_ratio = self.format_number(stock['pb_ratio'])
            else:
                pb_ratio = "n/a"

            if 'market_cap' in stock:
                market_cap = self.format_number(stock['market_cap'])
            else:
                market_cap = "n/a"

            if 'float_rotation' in stock:
                float_rotation = self.format_number(stock['float_rotation'])
            else:
                float_rotation = "n/a"


            print(f"{symbol}, ${price}, {percent_change}% -- pb_ratio: {pb_ratio}, mCap: {market_cap}, float_rotation: {float_rotation or 0}")
    
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

'''

    def getTopMovers(self, max_price=20, min_price=0.10, top_n=50):
        if not hasattr(self, 'movers'):
            self.movers = []

        headers = {
            "accept": "application/json",
            "APCA-API-KEY-ID": config.ALPACA_API_KEY,
            "APCA-API-SECRET-KEY": config.ALPACA_SECRET_KEY
        }

        # 1️⃣ Fetch movers
        url_movers = "https://data.alpaca.markets/v1beta1/screener/stocks/movers?top=50"
        movers_response = requests.get(url_movers, headers=headers)
        movers_data = movers_response.json()

        movers_list = []
        for mover_type in ["gainers", "losers"]:
            for item in movers_data.get(mover_type, []):
                price = item.get('price', 0)
                #print(f"{item.get('symbol')}")
                if min_price < price < max_price:
                    movers_list.append(item)

        # 2️⃣ Fetch most-actives
        url_active = "https://data.alpaca.markets/v1beta1/screener/stocks/most-actives"
        active_response = requests.get(url_active, headers=headers)
        active_data = active_response.json()
        most_actives = active_data.get('most_actives', active_data) if isinstance(active_data, dict) else active_data
        active_symbols = {item['symbol'] for item in most_actives}

        # 3️⃣ Merge: keep movers that are also in most-actives
        top_stocks = [item for item in movers_list if item['symbol'] in active_symbols]

        # Optionally: limit to top_n
        self.movers = top_stocks[:top_n]
        #return self.movers
    '''