# import requests
# from research.stockBot import stockBot
from data.symbolBot import SymbolBot
from data.fallbackCrypto import fallback_crypto
from datetime import datetime, timedelta

class CryptoBot:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.symbolBot = SymbolBot()
        self.symbolList = []

    def load_stocks(self):
        self.stockList 

    def load_symbols_from_symbolBot(self):
        self.symbolList = self.symbolBot.crypto_full_list()
    
    def load_symbols_from_fallback(self):
        self.symbolList = fallback_crypto

    def print_symbols(self):
        for symbol in self.symbolList: 
            print(
                symbol['symbol']
            )
        
    def print_symbols_and_price(self):
        for symbol in self.symbolList: 
            percentageChange = round(symbol['price_change_percentage_24h'], 2)
            currentPrice = round(symbol['current_price'], 3)
            print(
                symbol['symbol'] + ", $" + str(currentPrice) + ", " + str(percentageChange) + "%"
            )

    def print_symbols_and_price_by_amount(self, amount):
        for symbol in self.symbolList: 
            if(amount <= 0): break
            percentageChange = round(symbol['price_change_percentage_24h'], 2)
            currentPrice = round(symbol['current_price'], 3)
            print(
                symbol['symbol'] + ", $" + str(currentPrice) + ", " + str(percentageChange) + "%"
            )
            amount -= 1