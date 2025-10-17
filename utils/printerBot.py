class PrinterBot:

    def __init__(self):
        pass

    def displayStocks(self, list):
        for stock in list:
            print(stock['ticker'], ", Volume (", stock['volumeChange'], "%), prevClose: $",
                stock['prevClose'], ", latestClose: $", stock['latestClose'],
                ", priceChangePercentage: ", stock['priceChangePercentage'], "%" )

    def listStocks(self, list=["empty List.."], limit = 200):
        index = 0
        for stock in list:
            if(index == limit): break
            index += 1

            symbol = stock['symbol']
            price = self.format_number(stock['price'])
            percent_change = self.format_number(stock['percent_change'])

            if 'pb_ratio' in stock:
                pb_ratio = self.format_number(stock['pb_ratio'])
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
            
            if 'summary' in stock:
                summary = stock['summary'] or 0
            else:
                summary = "n/a"

            if 'headline' in stock:
                headline = stock['headline'] or 0
            else:
                headline = "n/a"

            #Skipping other_info to keep visual info simple
            '''
            if 'other_info' in stock:
                other_info = stock['other_info']
            else:
                other_info = "n/a"
            '''
            print(f"{symbol}, ${price}, {percent_change}% -- pb_ratio: {pb_ratio}, mCap: {market_cap}, float_rotation: {float_rotation or 0}\n"
                  f"headline: {headline}\n" 
                  f"summary: {summary}\n")

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