'''
    def populate_stockList(self, stocks):
        try:
            for stock in stocks:
                try:
'''
                    #The following three lines is one of the ways to get info from alpaca
'''
                    req = StockLatestQuoteRequest(symbol_or_symbols=stock['symbol'])
                    latest_trade = dataClient.get_stock_latest_trade(req)[stock['symbol']]
                    latest_price_alpaca = latest_trade.price
'''

'''

                    #print(f"stock['symbol']: {stock['symbol']}")
                    ticker = yf.Ticker(stock['symbol'])
                    fast_info = ticker.fast_info

                    '''
'''
                    # These contain more info but are generally considered too dense
                    info = ticker.info
                    cash_flow = ticker.cash_flow
                    income_statement = ticker.income_stmt
                    financials = ticker.financials
                    growth_estimates = ticker.growth_estimates
                    ''' 
'''

                    last_price = float(fast_info.get('lastPrice', 0))
                    previous_close = fast_info.get('previousClose', 0)
                    percent_change = 0
                    if previous_close:
                        percent_change = ((last_price - previous_close) / previous_close) * 100
                    percent_change = self.format_number(percent_change)


                    open = fast_info.get('open', 0)
                    price_target = ticker.analyst_price_targets.get('current', 0)
                    year_low = fast_info.get('yearLow', 0)
                    year_high = fast_info.get('yearHigh', 0)
                    fifty_day_average = fast_info.get('fiftyDayAverage', 0)
                    two_hundred_day_average = fast_info.get('twoHundredDayAverage', 0)
                    ten_day_volume = fast_info.get('tenDayAverageVolume', 0)
                    three_month_volume = fast_info.get('threeMonthAverageVolume', 0)
                    balance_sheet = ticker.balance_sheet if ticker.balance_sheet is not None else "n/a"
                    stock['other_info'] = ({
                        "symbol": stock['symbol'],
                        "last_price": self.format_number(last_price),
                        "open": self.format_number(open),
                        "analyst_price_target": self.format_number(price_target),
                        "year_low": self.format_number(year_low),
                        "year_high":self.format_number(year_high),
                        "fifty_day_average": self.format_number(fifty_day_average),
                        "two_hundred_day_average": self.format_number(two_hundred_day_average),
                        "ten_day_volume": self.format_number(ten_day_volume),
                        "three_month_volume": self.format_number(three_month_volume),
                        "balance_sheet": balance_sheet
                          })
                    if 'price' not in stock:
                        stock['price'] = last_price
                    if 'percent_change' not in stock:
                        stock['percent_change'] = percent_change

                except Exception as e:
                    print(f"Error in populate_stockList() for symbol: {stock['symbol']}: {e}")

        except Exception as e:
            print("Error in populate_stockList(): {e}")

        return stocks

'''
'''
    def fill_list(self):
        self.stockList = self.quick_fill()
        print("stock list found:")
        for item in self.stockList:
            print(f"Item: {item}")
'''
'''
    def populate_info_details(self, stocks):
        try:
            for stock in stocks:
                try:
                    ticker = yf.Ticker(stock['symbol'])
                    info = ticker.info
                    stock['info'] = info

                except Exception as e:
                    print(f"Error in populate_info_details() for symbol: {stock['symbol']}: {e}")

        except Exception as e:
            print("Error in populate_info_details(): {e}")

        return stocks
'''
'''
    def fill_stock_data_from_yfinance(self, tickers):
        today = datetime.now()
        lastWeek = today - timedelta(7)
        results = []

        # === Pull all history at once ===
        all_history = yf.download(tickers, group_by='ticker', threads=True)

        for ticker in all_history:
            try:
                results.append(all_history[ticker].tail())

            except Exception as e:
                print(f"Error retrieving data for {ticker}: {e}")
                continue

        self.stockList = results
        # return results
'''    
'''
    def quick_fill(self):
        tickers = self.symbolBot.stocks_full_list()
        return tickers
'''