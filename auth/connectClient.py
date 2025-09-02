import config

from alpaca.data.historical import NewsClient
from alpaca.trading.client import TradingClient
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient


newsClient = NewsClient(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY)
dataClient = StockHistoricalDataClient(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY)
paperTradingClient = TradingClient(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY, paper=True)
liveTradingClient = TradingClient(config.LIVE_ALPACA_API_KEY, config.LIVE_ALPACA_SECRET_KEY, paper=False)