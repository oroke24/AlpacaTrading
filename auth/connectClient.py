import config

from alpaca.trading.client import TradingClient
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient


dataClient = StockHistoricalDataClient(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY)
paperTradingClient = TradingClient(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY, paper=True)
liveTradingClient = TradingClient(config.LIVE_ALPACA_API_KEY, config.LIVE_ALPACA_SECRET_KEY, paper=False)