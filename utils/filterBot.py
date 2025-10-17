import yfinance as yf

class FilterBot():

    def __init__(self):
        pass

    def filter_shares_and_float(self, stocks, min_float=10_000_000, max_outstanding =1_000_000_000):
        filtered = []
        for stock in stocks:
            symbol = stock['symbol']
            percent_change = stock['percent_change']
            price = stock['price']
            market_cap = stock['market_cap']
            pb_ratio = stock['pb_ratio']

            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info or {}

                float_shares = info.get("floatShares")
                shares_outstanding = info.get("sharesOutstanding")
                volume = info.get("volume")

                if float_shares is None or shares_outstanding is None or volume is None:
                    #print(f"sym: {symbol}, float: {float_shares}, sharesOutstanding: {shares_outstanding} - Skipped")
                    continue

                float_rotation = round(volume/float_shares, 2)

                print(f"float_rotation for {symbol}: {float_rotation}")
                if float_rotation < 0.12 or float_rotation > 5.0:
                    #skip if too stagnant or speculative pump
                    continue

                if float_shares >= min_float and shares_outstanding <= max_outstanding:
                    #print(f"sym: {symbol}, float: {float_shares}, sharesOutstanding: {shares_outstanding} - Added")
                    filtered.append({
                                'symbol' : symbol,
                                'price' : price,
                                'percent_change' : percent_change,
                                'market_cap': market_cap,
                                'pb_ratio': pb_ratio,
                                'float_rotation': float_rotation
                    })

            except Exception as e:
                print(f"sym: {symbol}, Error: {e}")
        
        return filtered

        
    def filter_high_market_caps(self, stocks, cap_min=100_000_000, pe_max=30, pb_max=3.5, ps_max=10):
        filtered_stocks = []
        for stock in stocks:
            symbol = stock['symbol']

            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info or {}

                if 'price' in stock: price = stock['price']
                else: price = ticker.fast_info.get('lastPrice', 0)
                
                previous_close = ticker.fast_info.get('previousClose', 0)
                percent_change = 0
                if 'percent_change' in stock: percent_change = stock['percent_change']
                elif previous_close: percent_change = ((price - previous_close) / previous_close) * 100

                market_cap = info.get('marketCap')
                trailing_pe = info.get('trailingPE') or 0
                price_to_book = info.get('priceToBook')
                price_to_sales = info.get('priceToSalesTrailing12Months') or info.get('priceToSales') or 0

                #print(f"sym: {symbol}, mCap: {market_cap}, trailing_pe: {trailing_pe}, pb: {price_to_book}, ps: {price_to_sales}")

                if (market_cap is None or market_cap < cap_min):
                    # print(f"{symbol}: Market Cap too low or unavailable ({market_cap}).  Skipping.")
                    continue

                if (trailing_pe is not None and trailing_pe <= pe_max):
                    if(price_to_sales is not None and price_to_sales <= ps_max):
                        if(price_to_book is not None and 0 < price_to_book <= pb_max):
                            filtered_stocks.append({
                                'symbol' : symbol,
                                'price' : price,
                                'percent_change' : percent_change,
                                'market_cap': market_cap,
                                'pe_ratio': float(trailing_pe),
                                'ps_ratio': float(price_to_sales),
                                'pb_ratio' : float(price_to_book)
                            })
                            #print(f"{symbol}: Passed filters.  MCap: ${float(market_cap):,.2f}, P/E: {float(trailing_pe):.2f}, P/B: {float(price_to_book):.2f} - Added to list")
                            continue
                        else:
                            #print(f"{symbol}: P/B too high(over {pb_max}). P/B: {price_to_book}")
                            continue

            except Exception as e:
                print(f"Error processing {symbol}: {e}")
        return filtered_stocks