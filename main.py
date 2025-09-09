import sys
from research.cryptoBot.cryptoBot import CryptoBot
from research.stockBot.stockBot import StockBot
from research.aiBot.openAiBot import OpenAiBot
from research.newsBot.newsBot import get_latest_news
from data.symbolBot import SymbolBot
from utils.printerBot import PrinterBot
from utils.sorterBot import SorterBot
from utils.filterBot import FilterBot
from order.marketBuy import place_market_order_and_save_to_file, place_trailing_stops_from_local_file, calculate_position_size
from auth.connectClient import paperTradingClient, liveTradingClient
from datetime import datetime


def main():
    
    print("\n")
    if len(sys.argv) > 1 and sys.argv[1] == 'sell': 
        print(f"==================== Selling Process Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ====================")
        # Before buying, check yesterdays buys (if any) and place according sell positions
        print("Selling yesterdays positions.")
        place_trailing_stops_from_local_file()
        print(f"========================= Run End =========================")
        print("\n")
        return


    print("\n")
    print(f"==================== Buying Process Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ====================")

    live_account = liveTradingClient.get_account()
    buying_power = float(live_account.buying_power)
    day_trades = int(live_account.daytrade_count)

    if(day_trades >= 3):
        print(f"No trading today: Day Trade Count too high ({day_trades}), max allowed: 3")
        return

    # Initialize bots 
    filterBot = FilterBot()
    stockBot = StockBot()
    sorterBot = SorterBot()
    openAiBot = OpenAiBot()

    # --- StockBot Research and Trade Portion
    print(f"--- STOCK PORTION ---")

    # First, grab symbols worth looking at
    stockBot.getMovers(buying_power)
    stockBot.getMostActiveVolume(buying_power)


    # Then, filter best stocks to buy, if any.
    high_caps = filterBot.filter_high_market_caps(stockBot.stockList) #change to stockBot.movers if any issues arise
    print(f"Screened {len(stockBot.stockList)} => {len(high_caps)} passed market cap and price filter.")
    share_floats = filterBot.filter_shares_and_float(high_caps)
    print(f"Out of the {len(high_caps)}, {len(share_floats)} passed share and float filter.")

    print("Stocks worth buying are:")
    stocksToBuy = sorterBot.sort_price_low_to_high(share_floats)
    for stock in stocksToBuy:
        latest_news = get_latest_news(stock["symbol"])
        stock["headline"] = latest_news["headline"]
        stock["summary"] = latest_news["summary"]
    stockBot.listStocks(stocksToBuy)
    stocksLoadedInfo = stockBot.populate_stockList(stocksToBuy)

    print("openAi's Stock list:")
    openAi_opinion = openAiBot.studyStocks(stocksLoadedInfo, buying_power)
    print("\n=======   PLACING BUY ORDERS   =======")
    if not openAi_opinion:
        print("No AI approved stocks for today, rolling on without it")
        openAi_opinion = stocksToBuy[:2] #if ai fails just pull top two choices
    else:
        stockBot.listStocks(openAi_opinion)
    # Then, place orders

    '''
    for stockInfo in openAi_opinion:
        try:
            stockSymbol = stockInfo["symbol"].upper()
            place_market_order_and_save_to_file(stockSymbol)
        except Exception as e:
            print(f"Error fetching {stockInfo['symbol']} {e}...")
    # --- END StockBot Research and Trade Portion
    '''
    print(f"========================= Run End =========================")
    print("\n")
# ========== TESTING AREA ========== TESTING AREA =========== TESTING AREA ===========
def testing():

    print(f"==== Test Run Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ====")

    filterBot = FilterBot()
    stockBot = StockBot()
    sorterBot = SorterBot()
    openAiBot = OpenAiBot()
    
    '''
    cryptoBot = CryptoBot()
    symbolBot = SymbolBot()
    printerBot = PrinterBot()
    '''

    # --- StockBot Research and Trade Portion
    print(f"--- STOCK PORTION ---")

    stockBot.getMovers()
    stockBot.getMostActiveVolume()
    #list1 = stockBot.populate_stockList(stockBot.stockList)
    high_caps = filterBot.filter_high_market_caps(stockBot.stockList)
    print(f"Screened {len(stockBot.movers)} => {len(high_caps)} passed market cap and price filter.")
    share_floats = filterBot.filter_shares_and_float(high_caps)
    print(f"Out of the {len(high_caps)}, {len(share_floats)} passed share and float filter.")
    print("Stocks worth buying are:")
    stocksToBuy = sorterBot.sort_price_low_to_high(share_floats)
    for stock in stocksToBuy:
        latest_news = get_latest_news(stock["symbol"])
        stock["headline"] = latest_news["headline"]
        stock["summary"] = latest_news["summary"]
    stockBot.listStocks(stocksToBuy)
    #for symbol in stockBot.stockList:
    #    print(f"sym: {symbol['symbol']}, price: {symbol['price']}, %change: {symbol['percent_change']}")
    #stockBot.listStocks(list1[:7])
    #stockBot.listStocks(stockBot.movers)
    #print(f"{len(stockBot.movers)}")

    '''
    stock = stockBot.movers[0]
    latest_news = get_latest_news(stock["symbol"])
    print(f"latest_news: {latest_news}")
    stock["headline"] = latest_news['headline']
    stock["summary"] = latest_news['summary']
    print(stock)

    print(f"all movers ({len(stockBot.movers)})")
    stockBot.listStocks(stockBot.movers)

    positives = sorterBot.get_positives(stockBot.movers)
    negatives = sorterBot.get_negatives(stockBot.movers)

    listUptrend = sorterBot.sort_stock_by_upward_percent_change(stockBot.movers)
    listDowntrend = sorterBot.sort_stock_by_downward_percent_change(stockBot.movers)

    listLowToHigh = sorterBot.sort_price_low_to_high(stockBot.movers)
    listHighToLow = sorterBot.sort_price_high_to_low(stockBot.movers)

    stockBot.CheapUpTrenders = sorterBot.double_placers(positives, listLowToHigh)
    stockBot.CheapDownTrenders = sorterBot.double_placers(negatives, listLowToHigh)

    stockBot.ExpensiveUpTrenders = sorterBot.double_placers(listUptrend, listHighToLow)
    stockBot.ExpensiveDownTrenders = sorterBot.double_placers(listDowntrend, listHighToLow)

    '''
    #Testing Area (last edit 08/19/2025)

    '''
    print("cheap down trenders")
    stockBot.listStocks(stockBot.CheapDownTrenders)
    print("cheap up trenders")
    stockBot.listStocks(stockBot.CheapUpTrenders)
    print("expensive up trenders")
    stockBot.listStocks(stockBot.ExpensiveUpTrenders)
    print("expensive down trenders")
    stockBot.listStocks(stockBot.ExpensiveDownTrenders)

    print("Expensive trenders")
    stockBot.listStocks(listHighToLow, 10)
    print("Original Movers")
    stockBot.listStocks(stockBot.movers, 10)

    stockBot.listStocks(list3)
    print("Double Placers")
    stockBot.listStocks(stockBot.stockList)

    #End Testing Area -------------------

    # First, check yesterdays buys (if any) and place according sell positions
    # place_trailing_stops_from_local_file()
    '''

    '''
    live_account = liveTradingClient.get_account()
    buying_power = float(live_account.buying_power)

    #print(f"buying power - 10 = {float(live_account.buying_power) - 10:.2f}")

    #Then, place buy orders for today

    high_caps = filterBot.filter_high_market_caps(stockBot.movers)
    print(f"Screened {len(stockBot.movers)} => {len(high_caps)} passed market cap and price filter.")
    stockBot.listStocks(high_caps)
    share_floats = filterBot.filter_shares_and_float(high_caps)
    print(f"Out of the {len(high_caps)}, {len(share_floats)} passed share and float filter.")

    stocksToBuy = sorterBot.sort_price_low_to_high(share_floats)
    print(f"Stocks worth buying are:")
    stockBot.listStocks(stocksToBuy)

    for stock in stocksToBuy:
        pos_size = calculate_position_size(buying_power, stock['price'])
        print(f"Buying {pos_size} of {stock['symbol']}")
    '''



    '''
    openAi_opinion = openAiBot.studyStocks(stocksToBuy)
    print(f"openAi's Stock list:")
    stockBot.listStocks(openAi_opinion)
    for stock in openAi_opinion:
        pos_size = calculate_position_size(buying_power, stock['price'])
        print(
            f"{stock['symbol']}, ${stock['price']}, {stock['percent_change']}% "
            f"-- pb_ratio: {stock['pb_ratio']}, mCap: {stock['market_cap']}, float_rotation: {stock['float_rotation']}"
        )
        print(f"Buying {pos_size} of {stock['symbol']}")

    # This gets the top 5 biggest cheap gainers
    for stockInfo in stockBot.CheapUpTrenders[:5]:
        try:
            stockSymbol = stockInfo["symbol"].upper()
            place_market_order_and_save_to_file(stockSymbol, 1)
        except Exception as e:
            print(f"Error fetching {e}...")
    # This gets the top 5 biggest losers
    for stockInfo in stockBot.CheapDownTrenders[:5]:
        try:
            stockSymbol = stockInfo["symbol"].upper()
            place_market_order_and_save_to_file(stockSymbol, 1)
        except Exception as e:
            print(f"Error fetching {e}...")

    for stockInfo in high_caps:
        try:
            stockSymbol = stockInfo["symbol"].upper()
            place_market_order_and_save_to_file(stockSymbol, 1)
        except Exception as e:
            print(f"Error fetching {e}...")

    '''
    # --- END StockBot Research and Trade Portion
    '''
    # --- CrypoBot Research and Trade Portion
    print(f"--- CRYPTO PORTION ---")
    cryptoBot.load_symbols_from_symbolBot()

    list1 = sorterBot.sort_by_price_change_percentage_24h(cryptoBot.symbolList)
    list2 = sorterBot.sort_current_price_low_to_high(cryptoBot.symbolList)

    cryptoBot.symbolList = sorterBot.crypto_double_placers(list1, list2)
    cryptoBot.print_symbols_and_price()

    for cryptoInfo in cryptoBot.symbolList:
        try:
            cryptoSymbol = cryptoInfo["symbol"].upper() + "/USD"
            place_market_order_and_save_to_file(cryptoSymbol, 1, 2)
        except Exception as e:
            print(f"Error fetching {e}.. ")

    # --- END CrypoBot Research and Trade Portion
    '''
    print(f"==== Test Run End ====")

if __name__ == "__main__":
    main()
    #testing()