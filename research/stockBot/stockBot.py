import yfinance as yf
from datetime import datetime, timedelta

class StockBot:

    def __init__(self):
        pass

    def fill_stock_data_from_yfinance(self, list):
        today = datetime.now()
        yesterday = today - timedelta(1)
        lastWeek = today - timedelta(7)
        results = []

        for ticker in list:
            try:
                data = yf.Ticker(ticker)
            
                history = data.history(start=lastWeek, end=today)
                if history.empty:
                    continue
            
                latestVolume = int(history['Volume'].iloc[-1] or 0)

                if len(history) >= 2:
                    prevClose = round(history['Close'].iloc[-2], 2)
                    latestClose = round(history['Close'].iloc[-1], 2)
                    priceChangePercentage = round(((latestClose - prevClose) / prevClose)*100, 2)
                else:
                    prevClose = 0
                    latestClose = 0
                    priceChangePercentage = 0

                shares_df = data.get_shares_full(start=lastWeek, end=today)
                if shares_df is None or shares_df.empty:
                    print(f"No share count data for {ticker}")
                shareCount = int(shares_df.iloc[-1] or 0)

                if shareCount == 0:
                    print(f"Share count is 0 for {ticker}")
                    continue
            
                volumeChange = round(float((latestVolume/shareCount)*100), 2) # rounded 2 decimal places

                results.append({
                    'ticker': ticker,
                    'volume': latestVolume,
                    'shares': shareCount,
                    'volumeChange': volumeChange,
                    'prevClose': prevClose,
                    'latestClose': latestClose,
                    'priceChangePercentage': priceChangePercentage
                })

            except Exception as e:
                print(f"Error retrieving data for {ticker}: {e}")
                continue

        return results

