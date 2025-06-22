import requests
from data.symbolBot import SymbolBot
from data.fallbackCrypto import fallback_crypto
from datetime import datetime, timedelta

class CryptoBot:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.symbolBot = SymbolBot()
        self.symbolList = []

    def load_symbols_from_symbolBot(self):
        self.symbolList = self.symbolBot.crypto_full_list()
    
    def load_symbols_from_fallback(self):
        self.symbolList = fallback_crypto

    def print_symbols(self):
        for symbol in self.symbolList: 
            print(
                symbol
            )
        