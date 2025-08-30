import yfinance as yf
from auth.connectClient import dataClient
from alpaca.data import StockBarsRequest
from alpaca.data.timeframe import TimeFrame


class SorterBot:
    def __init__(self):
        pass

    def sort_by_volumeChange(self, list):
        return sorted(list, key=lambda s: s['volumeChange'], reverse=True)

    def sort_by_priceChange(self, list):
        return sorted(list, key=lambda s: s['priceChangePercentage'], reverse=True)

    def sort_stock_by_upward_percent_change(self, list):
        return sorted(list, key=lambda s: s['percent_change'], reverse=True)

    def sort_stock_by_downward_percent_change(self, list):
        return sorted(list, key=lambda s: s['percent_change'], reverse=False)

    def sort_by_price_change_percentage_24h(self, list):
        return sorted(list, key=lambda s: s['price_change_percentage_24h'], reverse=True)

    def sort_latest_close_low_to_high(self, list):
        return sorted(list, key=lambda s: s['latestClose'], reverse=False)
        
    def sort_price_low_to_high(self, list):
        return sorted(list, key=lambda s: s['price'], reverse=False)

    def sort_price_high_to_low(self, list):
        return sorted(list, key=lambda s: s['price'], reverse=True)

    def sort_current_price_low_to_high(self, list):
        return sorted(list, key=lambda s: s['current_price'], reverse=False)

    def sort_by_market_cap(self, list):
        # Sort descending by 'marketCap' if present, else 0
        return sorted(list, key=lambda s: s.get('marketCap', 0), reverse=True)

    def sort_by_volume(self, list):
        # Sort descending by 'volume' if present, else 0
        return sorted(list, key=lambda s: s.get('volume', 0), reverse=True)


    def double_placers(self, list1, list2):
        newList = []
        for index, i in enumerate(list1):
            if index > 25: break 
            for index, j in enumerate(list2):
                if index > 25: break
                if i['symbol'] == j['symbol']: newList.append(i)

        if newList.count == 0: newList.append("No double placers")
        return newList
        
    def crypto_double_placers(self, list1, list2):
        newList = []
        for index, i in enumerate(list1):
            if index > 50: break 
            for index, j in enumerate(list2):
                if index > 50: break
                if i['symbol'] == j['symbol']: 
                    newList.append(i)

        if newList.count == 0: newList.append("No double placers")
        return newList

    def passes_volume_filter(self, symbol, min_volume=500_000):
        try:
            print(f"Checking {symbol}...")

            request_params = StockBarsRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Day)
            barset = dataClient.get_stock_bars(request_params)
            print(barset)
            '''
            avg_volume = sum([bar.volume for bar in barset])
        
            print(f"{symbol} avg volume: {avg_volume:.0f}")
            return avg_volume >= min_volume
            '''
        except Exception as e:
            print(f"Could not fetch volume for {symbol}: {e}")
            return False
    
    def remove_low_volume_symbols(self, list, min_volume=500_000):
        new_list = []
        for symbol in list:
            if(not self.passes_volume_filter(symbol['symbol'], min_volume)):
                new_list.append(symbol)
            else:
                print(f"Removed {symbol} (low volume)")
        return new_list

        
