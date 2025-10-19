import yfinance as yf
from time import sleep

class InfoBot:
    def __init__(self):
        pass
    
    def populate_info(self, stocks, batch_size=100, pause=0.5):
        """
        Batch-fetch info, balancesheet, analyst targets, and first news summary.
        """
        try:
            # Uppercase symbols and map to stock dict
            symbol_to_stock = {stock['symbol'].upper(): stock for stock in stocks}
            symbols = list(symbol_to_stock.keys())

            # Process in batches
            for i in range(0, len(symbols), batch_size):
                batch = symbols[i:i + batch_size]
                tickers = yf.Tickers(" ".join(batch))

                for sym in batch:
                    stock = symbol_to_stock[sym]
                    t = tickers.tickers.get(sym)
                    if not t:
                        print(f"Ticker not found for symbol: {sym}")
                        stock['info'] = {}
                        stock['balance_sheet'] = {}
                        stock['price_target'] = {}
                        stock['news'] = None
                        continue

                    try:
                        # --- info ---
                        raw_info = t.info
                        stock['info'] = raw_info if isinstance(raw_info, dict) else {}
                        #print(stock['info'])

                        # --- balance sheet ---
                        raw_bs = t.balancesheet
                        # yf can return DataFrame
                        if hasattr(raw_bs, "to_dict"):
                            stock["balance_sheet"] = raw_bs.to_dict()
                        else:
                            stock["balance_sheet"] = {}

                        # --- price targets ---
                        raw_pt = t.analyst_price_targets
                        stock['price_target'] = raw_pt if isinstance(raw_pt, dict) else {}

                        # --- earnings date (reliable version via calendar) ---
                        try:
                            cal = t.calendar
                            if cal is not None:
                                stock['earnings_date'] = cal 
                            else:
                                stock['earnings_date'] = None
                        except Exception:
                            stock['earnings_date'] = None


                        # --- news summary (first one) ---
                        try:
                            news_list = t.news or []
                            if isinstance(news_list, list) and news_list:
                                content = news_list[0].get("content", {})
                                stock["news"] = content.get("summary")
                            else:
                                stock["news"] = None
                        except Exception:
                            stock["news"] = None

                    except Exception as e:
                        print(f"Error fetching info for {sym}: {e}")
                        stock['info'] = {}
                        stock['balance_sheet'] = {}
                        stock['price_target'] = {}
                        stock['news'] = None

                sleep(pause)  # gentle throttling between batches

        except Exception as e:
            print(f"Error in populate_info(): {e}")

        return self.assign_info_details(stocks)

    def assign_info_details(self, stocks):
        def safe_num(val, default=0.0):
            try:
                return float(val)
            except Exception:
                return default

        for stock in stocks:
            info = stock.get('info', {})

            float_shares = safe_num(info.get('floatShares'))
            shares_outstanding = safe_num(info.get('sharesOutstanding'))
            trailing_pe = safe_num(info.get('trailingPE'))
            price_to_book = safe_num(info.get('priceToBook'))
            price_to_sales = safe_num(
                info.get('priceToSalesTrailing12Months')
            ) or safe_num(info.get('priceToSales'))

            # volume was set earlier during populate_fast_info
            volume = safe_num(stock.get('volume', 0))
            float_rotation = ((volume / float_shares) * 100) if float_shares else 0

            stock['float_shares'] = round(float_shares)
            stock['shares_outstanding'] = round(shares_outstanding)
            stock['price_to_earnings'] = round(trailing_pe, 3)
            stock['price_to_book'] = round(price_to_book, 3)
            stock['price_to_sales'] = round(price_to_sales, 3)
            stock['float_rotation'] = round(float_rotation, 3)

        return stocks