import asyncio
from research.cryptoBot.cryptoBot import CryptoBot
from research.stockBot.stockBot import StockBot
from data.symbolBot import SymbolBot
from utils.printerBot import PrinterBot
from utils.sorterBot import SorterBot
from order.marketBuy import place_market_order_and_save_to_file, place_trailing_stops_from_local_file
from auth.connectClient import paperTradingClient
from datetime import datetime

def main():

    print(f"==== Run Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ====")

    stockBot = StockBot()
    sorterBot = SorterBot()
    '''
    cryptoBot = CryptoBot()
    symbolBot = SymbolBot()
    printerBot = PrinterBot()
    '''

    # --- StockBot Research and Trade Portion
    print(f"--- STOCK PORTION ---")

    stockBot.getMovers()

    '''
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

    '''
    #End Testing Area -------------------

    # First, check yesterdays buys (if any) and place according sell positions
    # place_trailing_stops_from_local_file()

    # Then, place buy orders for today
    high_caps = stockBot.filter_high_market_caps(stockBot.movers)
    print(f"Screened {len(stockBot.movers)} => {len(high_caps)} passed.")
    stockBot.listStocks(high_caps)

    '''
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
    '''

    for stockInfo in high_caps:
        try:
            stockSymbol = stockInfo["symbol"].upper()
            place_market_order_and_save_to_file(stockSymbol, 1)
        except Exception as e:
            print(f"Error fetching {e}...")

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
    print(f"==== Run End ====")

if __name__ == "__main__":
    main()