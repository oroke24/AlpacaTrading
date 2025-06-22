from data.getSP500 import getSP500
from data.getCrypto import get_crypto_tickers 
from data.watchLists import getLocalSymbols

class SymbolBot:
    def __init__(self, type='stock'):
        pass
        
    def stocks_full_list(self):
        fullList = getLocalSymbols()
        fullList += getSP500()
        return fullList
    
    def crypto_full_list(self):
        fullList = get_crypto_tickers()
        return fullList

    
    
