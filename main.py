from research.cryptoBot.cryptoBot import CryptoBot
from research.stockBot.stockBot import StockBot
from data.symbolBot import SymbolBot
from utils.printerBot import PrinterBot
from utils.sorterBot import SorterBot
from order.marketBuy import place_market_order_with_trailing_percentage

symbolBot = SymbolBot()
stockBot = StockBot()
cryptoBot = CryptoBot()
printerBot = PrinterBot()
sorterBot = SorterBot()
trendingStocks = []


cryptoBot.load_symbols_from_symbolBot()

list1 = sorterBot.sort_by_price_change_percentage_24h(cryptoBot.symbolList)
list2 = sorterBot.sort_current_price_low_to_high(cryptoBot.symbolList)

cryptoBot.symbolList = sorterBot.crypto_double_placers(list1, list2)
cryptoBot.print_symbols_and_price()

for cryptoInfo in cryptoBot.symbolList:
    try:
        place_market_order_with_trailing_percentage(cryptoInfo["symbol"].upper(), 1, 2)
    except Exception as e:
        print(f"Error fetching {e}.. ")
