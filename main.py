from research.cryptoBot.cryptoBot import CryptoBot



'''
from research.finhub.symbolInfo import get_quote, get_basic_technicals
from research.yfinance.getQuote import get_quote
from research.yfinance.getBasicTechnicals import get_basic_technicals
import time
import yfinance as yf
import pandas as pd
from data.symbols import MIDNIGHT6
from datetime import datetime, timedelta
from data.getSP500 import getSP500
from order.marketBuy import place_market_order_with_trailing_stop, place_market_order
'''
from research.stockBot.stockBot import StockBot
from data.symbolBot import SymbolBot
from utils.printerBot import PrinterBot
from utils.sorterBot import SorterBot

symbolBot = SymbolBot()
stockBot = StockBot()
cryptoBot = CryptoBot()
printerBot = PrinterBot()
sorterBot = SorterBot()
# scraperBot = ScraperBot()
trendingStocks = []
cryptoBot.load_symbols_from_fallback()
cryptoBot.print_symbols()

# print(symbolBot.stocks_full_list())
# print(symbolBot.crypto_full_listt())
# trendingStocks = stockBot.fill_stock_data_from_yfinance(symbolBot.crypto_full_list())
# cryptoList = symbolBot.crypto_full_list()

# trendingCrypto = cryptoBot.fill_crypto_data_from_coinGecko(cryptoList)
# trendingCrypto1 = sorterBot.sort_by_priceChange(trendingCrypto)
# trendingCrypto2 = sorterBot.sort_by_volume(trendingCrypto)
# silverCryptos = sorterBot.double_placers(trendingCrypto1, trendingCrypto2)
# silverCryptos = sorterBot.sort_price_low_to_high(trendingCrypto2)
# printerBot.displayCrypto(trendingCrypto)
# printerBot.displayCrypto(trendingCrypto)
'''
from research.scraperBot import ScraperBot 


for stock in scraperBot.get_top_gainers_yahoo():
    trendingStocks.append(stock['symbol'])

trendingStocks = yfinanceBot.fill_stock_data(trendingStocks)
trendingByVolume = sorterBot.sort_by_volumeChange(trendingStocks)
trendingByPrice = sorterBot.sort_by_priceChange(trendingStocks)
silverStocks = sorterBot.double_placers(trendingByVolume, trendingByPrice)
silverStocksLowToHigh = sorterBot.sort_price_low_to_high(silverStocks)

print("Volume Movers")
printerBot.display(trendingByVolume)
print("------------------------------------------------------------------")
print("Price Movers")
printerBot.display(trendingByPrice)
print("------------------------------------------------------------------")
print("silverStocks")
printerBot.display(silverStocksLowToHigh)
print("------------------------------------------------------------------")
print("stock to buy")
tickerToBuy = str(silverStocksLowToHigh[0]['ticker'])
print(silverStocksLowToHigh[0]['ticker'])



# place_market_order(tickerToBuy)
place_market_order_with_trailing_stop(tickerToBuy)
'''







