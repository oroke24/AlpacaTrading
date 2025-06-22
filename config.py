from dotenv import load_dotenv
import os

load_dotenv()

LIVE_ALPACA_API_KEY = os.getenv("LIVE_ALPACA_API_KEY")
LIVE_ALPACA_SECRET_KEY = os.getenv("LIVE_ALPACA_SECRET_KEY")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
CMC_PRO_API_KEY = os.getenv("CMC_PRO_API_KEY")
FINHUB_API_KEY = os.getenv("FINHUB_API_KEY")


