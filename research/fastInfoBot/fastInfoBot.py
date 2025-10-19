import yfinance as yf
from time import sleep

class FastInfoBot:

    def __init__(self):
        pass
    
    def populate_fast_info(self, stocks, batch_size=100, pause=0.5):
        """
        Batch-fetch fast_info for many stocks efficiently.
        - stocks: list of dicts, each with 'symbol' key
        - batch_size: number of symbols per batch request
        - pause: seconds to wait between batches
        """
        try:
            # Uppercase symbols and map to stock dict
            symbol_to_stock = {stock['symbol'].upper(): stock for stock in stocks}
            symbols = list(symbol_to_stock.keys())

            # Process in batches
            for i in range(0, len(symbols), batch_size):
                batch = symbols[i:i + batch_size]

                # Batch fetch tickers
                tickers = yf.Tickers(" ".join(batch))

                for sym in batch:
                    stock = symbol_to_stock[sym]
                    t = tickers.tickers.get(sym)
                    if t:
                        try:
                            # Safely fetch & immediately freeze dict 
                            if hasattr(t, "get_fast_info"):
                                info = t.get_fast_info() or {}
                            else:
                                info = {}

                            # Make 100% sure it's a real dict
                            stock["fast_info"] = dict(info)
                            #print(stock['fast_info'])
                        except Exception as e:
                            print(f"Error fetching fast_info for {sym}: {e}")
                            stock['fast_info'] = {}
                    else:
                        print(f"Ticker not found for symbol: {sym}")
                        stock['fast_info'] = {}

                sleep(pause)  # gentle throttling between batches

        except Exception as e:
            print(f"Error in populate_fast_info(): {e}")

        return self.assign_fast_info_details(stocks)

    def assign_fast_info_details(self, stocks):
        filtered = []
        for stock in stocks:

            fast = stock.get('fast_info')
            if not isinstance(fast, dict) or not fast:
                print(f"Skipping {stock['symbol']} in assign_fast_info_details(): might be delisted.")
                continue

            # Each field is isolated to prevent crash on missing keys
            def safe_get(key, default=0):
                try:
                    return fast.get(key, default) or default
                except Exception:
                    return default

            price = safe_get('lastPrice', 0)
            previous_close = safe_get('previousClose', 0)
            market_cap = safe_get('marketCap', 0)
            volume = safe_get('lastVolume', 0)
            tenDayVolume = safe_get('tenDayAverageVolume', 0)
            threeMonthAverageVolume = safe_get('threeMonthAverageVolume', 0)
            shares = safe_get('shares', 0)
            fiftyDayAvg = safe_get('fiftyDayAverage', 0)
            twoHundredDayAvg = safe_get('twoHundredDayAverage', 0)
            yearLow = safe_get('yearLow', 0)

            #-- Local caculations --
            percent_change = 0
            if(previous_close != 0): percent_change = ((price - previous_close)/previous_close) * 100  
            #-- End Local caculations --

            stock['price'] = round(price, 2)
            stock['previous_close'] = round(previous_close, 2)
            stock['percent_change'] = round(percent_change, 2)
            stock['market_cap'] = round(market_cap)
            stock['volume'] = round(volume)
            stock['ten_day_volume'] = round(tenDayVolume)
            stock['three_month_volume'] = round(threeMonthAverageVolume)
            stock['shares'] = round(shares)
            stock['fifty_day_average'] = round(fiftyDayAvg, 2)
            stock['two_hundred_day_average'] = round(twoHundredDayAvg, 2)
            stock['year_low'] = round(yearLow, 2)


            filtered.append(stock)

        return filtered