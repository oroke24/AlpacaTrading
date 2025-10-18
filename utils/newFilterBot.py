import yfinance as yf
import time
from itertools import islice

class NewFilterBot:

    def __init__(self):
        pass

    @staticmethod
    def chunked(iterable, n):
        it = iter(iterable)
        while True:
            chunk = list(islice(it, n))
            if not chunk:
                break
            yield chunk

    def fetch_data_for_stocks(self, stocks, batch_size=50, sleep_time=2):
        """
        Fetches batch market data for stocks and enriches input dicts with key info.
        Returns the updated list with fetched info.
        """
        symbols = [stock['symbol'] for stock in stocks]
        enriched_stocks = []

        for batch_symbols in self.chunked(symbols, batch_size):
            batch_str = " ".join(batch_symbols)
            try:
                batch_data = yf.download(batch_str, period="1d", group_by="ticker", progress=False, threads=True, auto_adjust=True)
                # Normalize data structure for single vs multiple tickers
                if len(batch_symbols) == 1:
                    batch_data = {batch_symbols[0]: batch_data}
                else:
                    batch_data = {ticker: batch_data[ticker] for ticker in batch_symbols if ticker in batch_data.columns.levels[0]}

            except Exception as e:
                print(f"Error downloading batch {batch_symbols[0]} - {batch_symbols[-1]}: {e}")
                continue

            for symbol in batch_symbols:
                stock = next((s for s in stocks if s['symbol'] == symbol), None)
                if not stock:
                    continue
                try:
                    # Use yfinance Ticker once per symbol for fundamental info
                    ticker_obj = yf.Ticker(symbol)
                    info = ticker_obj.info or {}
                    fastInfo = ticker_obj.fast_info or {}
                    #print(f"info: {info}\n")
                    #print(f"fastInfo: {fastInfo}\n")

                    # Enrich stock with fundamental data
                    stock['symbol'] = symbol
                    stock['price'] = info.get("currentPrice") or 0 
                    stock['float_shares'] = info.get("floatShares") or 0 #fastInfo.get("floatShares") or 0
                    stock['shares_outstanding'] = info.get("sharesOutstanding") or 0 # fastInfo.get("sharesOutstanding") or 0
                    stock['volume'] = info.get("volume") or 0 # fastInfo.get("volume") or 0
                    stock['market_cap'] = info.get("marketCap") or 0 # fastInfo.get("marketCap") or 0
                    stock['pe_ratio'] = info.get("trailingPE") or 0 # fastInfo.get("trailingPE") or 0
                    stock['pb_ratio'] = info.get("priceToBook") or 0 # fastInfo.get("priceToBook") or 0
                    stock['ps_ratio'] = info.get("priceToSalesTrailing12Months") or 0 # info.get("priceToSales") or 0
                    stock['float_rotation'] = round(stock['volume'] / stock['float_shares'], 3)
                    print(f"{symbol}: {stock}")

                    # Add price, percent_change from batch_data if available
                    if symbol in batch_data:
                        df = batch_data[symbol]
                        #print(f"df: {df}")
                        stock['price'] = round(df['Close'].iloc[-1],2) if not df.empty else 0
                        #print(f"{symbol}: ${stock['price']}")
                        if len(df) > 1:
                            previous_close = df['Close'].iloc[-2] or 0
                            stock['percent_change'] = ((stock['price'] - previous_close) / previous_close) * 100 if previous_close else 0
                        else:
                            stock['percent_change'] = stock.get('percent_change', 0)
                    print(f"{symbol} info: {stock}")
                    enriched_stocks.append(stock)
                except Exception as e:
                    print(f"Error fetching info for {symbol}: {e}")

            time.sleep(sleep_time)

        return enriched_stocks

    def filter_shares_and_float(self, stocks, min_float=10_000_000, max_outstanding=1_000_000_000):
        filtered = []
        for stock in stocks:
            float_shares = stock.get('floatShares')
            shares_outstanding = stock.get('sharesOutstanding')
            volume = stock.get('volume')
            if not float_shares or not shares_outstanding or not volume:
                continue
            if not (0.12 <= stock['float_rotation'] <= 5.0):
                continue
            if float_shares >= min_float and shares_outstanding <= max_outstanding:
                filtered.append(stock)
        return filtered

    def filter_high_market_caps(self, stocks, cap_min=100_000_000, pe_max=30, pb_max=3.5, ps_max=10):
        filtered_stocks = []
        for stock in stocks:
            market_cap = stock.get('marketCap') 
            trailing_pe = stock.get('trailingPE')
            price_to_book = stock.get('priceToBook')
            price_to_sales = stock.get('priceToSalesTrailing12Months')
            if not market_cap or market_cap < cap_min:
                print(f"{stock['symbol']} market cap check failed: {market_cap}")
                continue
            print(f"{stock['symbol']} passed market cap: {market_cap}")
            filtered_stocks.append(stock)
            print(f"{stock['symbol']} trailing_pe: {trailing_pe}, pb: {price_to_book}, ps: {price_to_sales}")
            '''
            if trailing_pe <= pe_max and 0 < price_to_book <= pb_max and price_to_sales <= ps_max:
                filtered_stocks.append(stock)
            '''
        return filtered_stocks
