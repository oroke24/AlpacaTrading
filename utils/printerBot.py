class PrinterBot:

    def __init__(self):
        pass

    def displayStocks(self, list):
        for stock in list:
            print(stock['ticker'], ", Volume (", stock['volumeChange'], "%), prevClose: $",
                stock['prevClose'], ", latestClose: $", stock['latestClose'],
                ", priceChangePercentage: ", stock['priceChangePercentage'], "%" )

    def simpleList(self, list=["empty List.."]):
        for stock in list:
            sym = stock['symbol']
            price = stock['price']
            pct = stock['percent_change']
            market_cap = self.format_number(stock['market_cap'])
            pb_ratio = self.format_number(stock['price_to_book'])
            volume = self.format_number(stock['volume'])
            float_shares = self.format_number(stock['float_shares'])
            float_rotation = self.format_number(stock['float_rotation'])
            fifty_avg = self.format_number(stock['fifty_day_average'])
            low = self.format_number(stock['year_low'])
            print(f"{sym}, pct: {pct}%, ${price}, 50_avg: ${fifty_avg}, yr_low: ${low} -- mCap: {market_cap}, pb_ratio: {pb_ratio} -- vol: {volume}, f_shares: {float_shares}, f_r%: {float_rotation}%")

    def listStocks(self, list=["empty List.."]):
        for stock in list:

            symbol = stock['symbol']
            price = self.format_number(stock['price'])
            percent_change = self.format_number(stock['percent_change'])

            if 'price_to_book' in stock:
                pb_ratio = self.format_number(stock['price_to_book'])
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
            
            if 'news' in stock:
                news = stock['news'] or 0
            else:
                news = "n/a"
            
            if 'price_target' in stock:
                price_target = stock['price_target'] or 0
            else:
                price_target = "n/a"

            if 'earnings_date' in stock:
                earnings_date = stock['earnings_date'] or 0
            else:
                earnings_date = "n/a"

            #Skipping other_info to keep visual info simple
            '''
            if 'other_info' in stock:
                other_info = stock['other_info']
            else:
                other_info = "n/a"
            '''
            print(f"{symbol}, ${price}, {percent_change}% -- pb_ratio: {pb_ratio}, mCap: {market_cap}, float_rotation: {float_rotation}%,\n"
                  f" earnings_date: {earnings_date}\n" 
                  f" analyst_price_target: {price_target}\n" 
                  f"news: {news}\n")

    def displayCrypto(self, list):
        for crypto in list:
            print(crypto['ticker'], 
                  ", Volume (", crypto['volume'],"%)",
                  ", latestClose: $", crypto['latestClose'],
                  ", priceChangePercentage: ", crypto['priceChangePercentage'], "%" )

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