import sys
import os
import time
from research.stockBot.stockBot import StockBot
from research.aiBot.openAiBot import OpenAiBot
from research.fastInfoBot.fastInfoBot import FastInfoBot
from research.infoBot.infoBot import InfoBot
from data.symbolBot import SymbolBot
from utils.printerBot import PrinterBot
from utils.sorterBot import SorterBot
from utils.filterBot import FilterBot
from order.buyingBot import BuyingBot
from order.sellingBot import SellingBot

from auth.connectClient import paperTradingClient, liveTradingClient
from datetime import datetime

RESTRICTED_POSITIONS_FILE = "restricted_positions.json"

def main():

    # Initialize bots  
    stockBot = StockBot()
    buyingBot = BuyingBot()
    sellingBot = SellingBot()
    filterBot = FilterBot()
    printerBot = PrinterBot()
    sorterBot = SorterBot()
    openAiBot = OpenAiBot()
    symbolBot = SymbolBot()
    fastInfoBot = FastInfoBot()
    infoBot = InfoBot()
    
    print("\n")

    if len(sys.argv) > 1 and sys.argv[1] == 'sell': 
        stockBot.add_equity_to_history()
        print(f"==================== Selling Process Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ====================")
        # --- Reset restricted positions for a new day ---
        if os.path.exists(RESTRICTED_POSITIONS_FILE):
            os.remove(RESTRICTED_POSITIONS_FILE)
            print("Cleared restricted positions for a new day.")
        # Before buying, check yesterdays buys (if any) and place according sell positions
        print("Selling yesterdays positions.")
        sellingBot.place_trailing_stops_from_local_file()
        print(f"========================= Run End =========================")
        print("\n")
        return

    print("\n")
    startTime = datetime.now()
    startTimeFormatted = startTime.strftime('%Y-%m-%d %H:%M:%S')
    print(f"==================== Buying Process Started: {startTimeFormatted} ====================")

    live_account = liveTradingClient.get_account()
    buying_power = float(live_account.buying_power)
    day_trades = int(live_account.daytrade_count)

    if(day_trades >= 3):
        print(f"No trading today: Day Trade Count too high ({day_trades}), max allowed: 3")
        return

    # --- StockBot Research and Trade Portion
    print(f"--- STOCK PORTION ---")

    #--- Initialize symbols ---#
    print(f"Getting symobls..")
    stockBot.stockList = symbolBot.stocks_full_list()
    stockBot.getMovers(buying_power)
    stockBot.getMostActiveVolume(buying_power)

    #--- Get the desired list of symbols ---#
    stocks = stockBot.stockList #add '[:number]' to end to shorten list for testing.  EX: stockBot.stockList[:25] 
    print(f"Got {len(stocks)} symobls..")

    #--- Efficient populate and filter ---#
    print(f"Getting 'fast_info' for each symbol. Might take a while..")
    stocks = fastInfoBot.populate_fast_info(stocks)

    #--- First set of filters ---#
    stocks = filterBot.filter_price_range(stocks, buying_power)
    stocks = filterBot.filter_out_small_market_caps(stocks)
    stocks = filterBot.filter_out_small_volume(stocks)
    stocks = filterBot.filter_by_moving_averages(stocks)
    stocks = filterBot.filter_above_year_low(stocks)

    print(f"fast_info filters complete.\n"
          f"{len(stocks)} will now be populated with heavier 'populate_info'.\n")

    #--- Expensive populate and filter ---#
    stocks = infoBot.populate_info(stocks)
    stocks = filterBot.filter_price_to_earnings(stocks)
    stocks = filterBot.filter_price_to_book(stocks)
    stocks = filterBot.filter_price_to_sales(stocks)
    stocks = filterBot.filter_float_rotation(stocks)
    print(f"Heavier filters complete.\n")

    print("Stocks worth buying are:")
    stocks = sorterBot.sort_fifty_day_ma_momentum_high_to_low(stocks)
    printerBot.simpleList(stocks)
    print("\n")
    stocks = stockBot.grab_snapshots(stocks)

    '''
    print("--------RAW STOCK DATA----------")
    for stock in stocks:
        print(stock)
    '''

    #--- Ask Ai ---#
    print("openAi's Stock list:")
    openAi_opinion = openAiBot.studyStocks(stocks, buying_power)
    print("\n=======   PLACING BUY ORDERS   =======")
    if not openAi_opinion:
        print("No AI approved stocks for today, rolling on without it")
        openAi_opinion = stocks #if ai fails just pull from stocks to buy
    printerBot.moderateListWithNews(openAi_opinion)

    #--- Place orders ---#
    for stockInfo in openAi_opinion:
        try:
            stockSymbol = stockInfo["symbol"].upper()
            buyingBot.place_market_order_and_save_to_file(stockSymbol)
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching {stockInfo['symbol']} {e}...")
    # --- END StockBot Research and Trade Portion
    '''
    '''
    print(f"========================= Run End =========================")
    endTime = datetime.now()
    timeDiff = endTime - startTime
    elapsed_seconds = timeDiff.total_seconds()
    minutes, seconds = divmod(elapsed_seconds, 60)
    print(f"(Execution time: {int(minutes)}m {seconds:.2f}s)")
    print("\n")
# ========== TESTING AREA ========== TESTING AREA =========== TESTING AREA ===========
def testing():

    print(f"==== Test Run Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ====")
    stockBot = StockBot()
    stockBot.add_equity_to_history()
    print(f"==== Test Run End ====")

if __name__ == "__main__":
    main()
    #testing()