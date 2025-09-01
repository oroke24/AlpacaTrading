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
        url = "https://data.alpaca.markets/v1beta1/screener/stocks/movers?top=50"
        headers = {"accept": "application/json",
                   "APCA-API-KEY-ID": config.ALPACA_API_KEY,
                   "APCA-API-SECRET-KEY": config.ALPACA_SECRET_KEY}
        response = requests.get(url, headers=headers)
        # print(response.text)
        data = response.json()
        '''
        for item in response:
            print(item)
        '''
        for mover_type in ["gainers", "losers"]:
            # print(f"\n---{mover_type.upper()} ---")

            for item in data[mover_type]:
                # print(f"Symbol: {item['symbol']}, Price: {item['price']}, Change: {item['percent_change']}%")
                if(min_price < item['price'] < max_price): self.movers.append(item)

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
