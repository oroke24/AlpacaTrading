import yfinance as yf

class FilterBot():

    def __init__(self):
        pass

    # --- Following filters require populate_fast_info() from stockBot
    def filter_price_range(self, stocks, buying_power):
        #print(f"Size before price range filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks:
            price = stock.get('price')
            try:
                if price and (0.02 < price < buying_power/2):
                    filtered.append(stock)
            except Exception:
                # skip malformed price values
                continue
        print(f"Size after price range filter: {len(filtered)}\n")
        return filtered 

    def filter_out_small_market_caps(self, stocks, cap_min=50_000_000):
        #print(f"Size before small cap filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks:
            cap = stock.get('market_cap')
            try:
                if cap and (cap_min < cap):
                    filtered.append(stock)
            except Exception:
                continue
        print(f"Size after small cap filter: {len(filtered)}\n")
        return filtered 

    def filter_out_small_volume(self, stocks, vol_min=500_000):
        #print(f"Size before volume filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks:
            vol = stock.get('volume')
            try:
                if vol and (vol > vol_min):
                    filtered.append(stock)
            except Exception:
                continue
        print(f"Size after volume filter: {len(filtered)}\n")
        return filtered 
    
    def filter_relative_strength(self, stocks, change_min=5.0):
        """
        Keep stocks with at least -15% daily change.
        Helps catch late-day runners that often gap up.
        """
        #print(f"Size before relative strength filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks:
            pct_change = stock.get('percent_change', 0)
            try:
                if pct_change and (pct_change < change_min):
                    filtered.append(stock)
            except Exception:
                continue
        print(f"Size after relative strength filter: {len(filtered)}\n")
        return filtered
    
    # --- Following filters require populate__info() from stockBot

    def filter_price_to_earnings(self, stocks, pe_max=30):
        #print(f"Size before price to earnings filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks:
            price_to_earnings = stock.get('price_to_earnings')
            try:
                if price_to_earnings and (price_to_earnings < pe_max):
                    filtered.append(stock)
            except Exception:
                continue
        print(f"Size after price to earnings filter: {len(filtered)}\n")
        return filtered

    def filter_price_to_book(self, stocks, pb_min = 0, pb_max=3.5):
        #print(f"Size before price to book filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks:
            price_to_book = stock.get('price_to_book')
            try:
                if price_to_book and (pb_min < price_to_book < pb_max):
                    filtered.append(stock)
            except Exception:
                continue
        print(f"Size after price to book filter: {len(filtered)}\n")
        return filtered
    
    def filter_price_to_sales(self, stocks, ps_max=10):
        #print(f"Size before price to sales filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks:
            price_to_sales = stock.get('price_to_sales')
            try:
                if price_to_sales and (price_to_sales < ps_max):
                    filtered.append(stock)
            except Exception:
                continue
        print(f"Size after price to sales filter: {len(filtered)}\n")
        return filtered
    

    def filter_float_rotation(self, stocks, rotation_pct_min=1.5, rotation_pct_max=100):
        #print(f"Size before float rotation filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks:
            float_rotation_pct = stock.get('float_rotation')
            try:
                if float_rotation_pct and (rotation_pct_min < float_rotation_pct < rotation_pct_max):
                    filtered.append(stock)
            except Exception:
                continue
        print(f"Size after float rotation filter: {len(filtered)}\n")
        return filtered
    
    def filter_by_moving_averages(self, stocks):
        #print(f"Size before moving average filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks:
            price = stock.get('price')
            ma50 = stock.get('fifty_day_average')
            ma200 = stock.get('two_hundred_day_average')

            try:
                if price and ma50 and ma200 and (price > ma50 > ma200):
                    filtered.append(stock)
            except Exception:
                continue

        print(f"Size after moving average filter: {len(filtered)}\n")
        return filtered

    def filter_above_year_low(self, stocks, pct_above_low=0.15):
        #print(f"Size before 52-week low filter: {len(stocks)}")
        filtered = []
        print("filtering...")
        for stock in stocks:
            price = stock.get('price')
            year_low = stock.get('year_low')

            try:
                if price and year_low:
                    if price > year_low * (1 + pct_above_low):
                        filtered.append(stock)
            except Exception:
                continue

        print(f"Size after 52-week low filter: {len(filtered)}\n")
        return filtered

    # --- Tiny helpers (minimal, low-risk additions) ---
    def simple_score(self, stock):
        """
        Small, fast score using percent_change and approximate dollar volume.
        Returns a float score (higher is better). Uses only snapshot fields.
        """
        try:
            pct = stock.get('percent_change') or 0.0
            price = stock.get('price') or 0.0
            vol10 = stock.get('ten_day_volume') or stock.get('three_month_volume') or stock.get('volume') or 0

            # normalize percent: 0..10% -> 0..1
            pct_score = max(min(pct / 10.0, 1.0), -1.0)
            pct_score = max(pct_score, 0.0)

            # dollar vol normalized: 0..1M -> 0..1
            dollar_vol = price * vol10
            dv_score = min(dollar_vol / 1_000_000.0, 1.0)

            # weighted
            return pct_score * 0.6 + dv_score * 0.4
        except Exception:
            return 0.0

    def pick_top(self, stocks, top_n=10):
        """
        Return top_n stocks sorted by `simple_score`. Non-destructive.
        Adds '_simple_score' to copies of returned stock dicts.
        """
        scored = []
        for s in stocks:
            try:
                sc = self.simple_score(s)
            except Exception:
                sc = 0.0
            s_copy = s.copy()
            s_copy['_simple_score'] = sc
            scored.append(s_copy)

        scored.sort(key=lambda x: x.get('_simple_score', 0), reverse=True)
        return scored[:top_n]

