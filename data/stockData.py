class StockData:
    def __init__(self):
        pass
    
    def initialize_empty_stocks(self, stocks):
        for stock in stocks:
                message = "empty"
                stock['price'] = message 
                stock['previous_close'] = message
                stock['percent_change'] = message 
                stock['market_cap'] = message 
                stock['volume'] = message 
                stock['ten_day_volume'] = message 
                stock['three_month_volume'] = message  
                stock['shares'] = message 
                stock['float_shares'] = message
                stock['shares_outstanding'] = message
                stock['price_to_earnings'] = message
                stock['price_to_book'] = message
                stock['price_to_sales'] = message
                stock['float_rotation'] = message
                stock['fifty_day_average'] = message
                stock['two_hundred_day_average'] = message
                stock['year_low'] = message
                stock['balance_sheet'] = message
                stock['price_target'] = message
                stock['earnings_date'] = message
                stock['news'] = message
                
                #stock[''] = stock['info'].get('') or

        return stocks