class PrinterBot:

    def __init__(self):
        pass

    def displayStocks(self, list):
        for stock in list:
            print(stock['ticker'], ", Volume (", stock['volumeChange'], "%), prevClose: $",
                stock['prevClose'], ", latestClose: $", stock['latestClose'],
                ", priceChangePercentage: ", stock['priceChangePercentage'], "%" )

    def displayCrypto(self, list):
        for crypto in list:
            print(crypto['ticker'], 
                  ", Volume (", crypto['volume'],"%)",
                  ", latestClose: $", crypto['latestClose'],
                  ", priceChangePercentage: ", crypto['priceChangePercentage'], "%" )