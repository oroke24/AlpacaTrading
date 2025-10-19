import yfinance as yf

class FilterBot():

    def __init__(self):
        pass

    # --- Following filters require populate_fast_info() from stockBot
    def filter_price_range(self, stocks, buying_power):
        print(f"Size before price range filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks: 
            price = stock['price'] 
            if (0.1 < price < buying_power/2): filtered.append(stock)
        print(f"Size after price range filter: {len(filtered)}\n")
        return filtered 

    def filter_out_small_market_caps(self, stocks, cap_min=100_000_000):
        print(f"Size before small cap filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks: 
            cap = stock['market_cap'] 
            if (cap_min < cap): filtered.append(stock)
        print(f"Size after small cap filter: {len(filtered)}\n")
        return filtered 

    def filter_out_small_volume(self, stocks, vol_min=100_000):
        print(f"Size before volume filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks: 
            vol = stock['volume'] 
            if (vol_min < vol): filtered.append(stock)
        print(f"Size after volume filter: {len(filtered)}\n")
        return filtered 
    
    # --- Following filters require populate__info() from stockBot

    def filter_price_to_earnings(self, stocks, pe_max=30):
        print(f"Size before price to earnings filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks:
            price_to_earnings = stock['price_to_earnings']
            if price_to_earnings < pe_max:
                filtered.append(stock)
        print(f"Size after price to earnings filter: {len(filtered)}\n")
        return filtered

    def filter_price_to_book(self, stocks, pb_min = 0, pb_max=3.5):
        print(f"Size before price to book filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks:
            price_to_book = stock['price_to_book']
            if pb_min < price_to_book < pb_max:
                filtered.append(stock)
        print(f"Size after price to book filter: {len(filtered)}\n")
        return filtered
    
    def filter_price_to_sales(self, stocks, ps_max=10):
        print(f"Size before price to sales filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks:
            price_to_sales = stock['price_to_sales']
            if price_to_sales < ps_max:
                filtered.append(stock)
        print(f"Size after price to sales filter: {len(filtered)}\n")
        return filtered

    def filter_float_rotation(self, stocks, rotation_pct_min=1.5, rotation_pct_max=35):
        print(f"Size before float rotation filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks:
            float_rotation_pct = stock['float_rotation']
            if rotation_pct_min < float_rotation_pct < rotation_pct_max:
                filtered.append(stock)
        print(f"Size after float rotation filter: {len(filtered)}\n")
        return filtered
    
    def filter_by_moving_averages(self, stocks):
        print(f"Size before moving average filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks:
            price = stock['price']
            ma50 = stock['fifty_day_average']
            ma200 = stock['two_hundred_day_average']

            if price and ma50 and price > ma50:
                filtered.append(stock)

        print(f"Size after moving average filter: {len(filtered)}\n")
        return filtered

    def filter_above_year_low(self, stocks, pct_above_low=0.10):
        print(f"Size before 52-week low filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks:
            price = stock['price']
            year_low = stock['year_low']
        
            if price and year_low:
                if price > year_low * (1 + pct_above_low):
                    filtered.append(stock)

        print(f"Size after 52-week low filter: {len(filtered)}\n")
        return filtered

