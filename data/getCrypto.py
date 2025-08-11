import requests
from data.fallbackCrypto import fallback_crypto

def get_crypto_tickers(limit=150):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": False
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Return only the symbols, e.g., ['BTC', 'ETH', 'BNB']
        # print([coin["symbol"].upper() for coin in data])
        with open("data/fallbackCrypto.py", "w") as f:
            f.write("fallback_crypto = " + repr([coin for coin in data]))
        return [coin for coin in data]

    except Exception as e:
        print("Could not fetch live crypto data. Using fallback.")
        return fallback_crypto