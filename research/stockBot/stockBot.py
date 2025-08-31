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

    def filter_high_market_caps(self, stocks, cap_min=100_000_000, pe_max=20, pb_max=3, ps_max=4):
        print("hello from high cap filter")
        filtered_stocks = []
        for stock in stocks:
            symbol = stock['symbol']
            percent_change = stock['percent_change']
            price = stock['price']

            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info or {}

                market_cap = info.get('marketCap')
                trailing_pe = info.get('trailingPE')
                price_to_book = info.get('priceToBook')
                price_to_sales = info.get('priceToSalesTrailing12Months') or info.get('priceToSales')

                if (market_cap is None or market_cap < cap_min):
                    # print(f"{symbol}: Market Cap too low or unavailable ({market_cap}).  Skipping.")
                    continue

                if (trailing_pe is not None and trailing_pe <= pe_max):
                    if(price_to_book is not None and price_to_book <= pb_max):
                        filtered_stocks.append({
                            'symbol' : symbol,
                            'price' : price,
                            'percent_change' : percent_change,
                            'market_cap': market_cap,
                            'pe_ratio': float(trailing_pe),
                            'pb_ratio' : float(price_to_book)
                            
                        })
                        #print(f"{symbol}: Passed P/E and P/B filters.  MCap: ${float(market_cap):,.2f}, P/E: {float(trailing_pe):.2f}, P/B: {float(price_to_book):.2f} - Added to list")
                        continue
                    else:
                        #print(f"{symbol}: P/B too high(over {pb_max}). P/B: {price_to_book}")
                        continue
                
                elif(price_to_sales is not None and price_to_sales <= ps_max):
                    if(price_to_book is not None and price_to_book <= pb_max):
                        filtered_stocks.append({
                            'symbol' : symbol,
                            'price' : price,
                            'percent_change' : percent_change,
                            'market_cap': market_cap,
                            'ps_ratio': float(price_to_sales),
                            'pb_ratio' : float(price_to_book)
                        })
                        #print(f"{symbol}: Passed P/S and P/B filters. Added to list.")
                        continue
                    else:
                        #print(f"{symbol}: P/B too high(over {pb_max}). P/B: {price_to_book}")
                        continue
                
                '''
                else:
                    print(f"{symbol}: Did not pass all filters")
                    if market_cap is None or market_cap < cap_min:
                        print(f"  - Market cap is unavailable or too low: {market_cap}")
                    if trailing_pe is None or trailing_pe > pe_max:
                        print(f"  - P/E is unavailable or too high: {trailing_pe}")
                    if price_to_sales is None or price_to_sales > ps_max:
                        print(f"  -P/S is unavailable or too high: {price_to_sales}")
                    if price_to_book is None or price_to_book > pb_max:
                        print(f"  - P/B is unavailable or too high: {price_to_book}")
                '''

            except Exception as e:
                print(f"Error processing {symbol}: {e}")
        return filtered_stocks
    
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
    
    def getMovers(self, min_price=.10, max_price=20):
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
            print(f"{stock}")
    
    def format_mcap(value):
        if value is None:
            return "N/A"
        if value >= 1_000_000_000:
            return f"${value / 1_000_000_000:.1f}B"
        elif value >= 1_000_000:
            return f"${value / 1_000_000:.1f}M"
        else:
            return f"${value:,}"
