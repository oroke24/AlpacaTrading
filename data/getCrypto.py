import requests
from data.fallbackCrypto import fallback_crypto

def get_crypto_tickers(limit=100):
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
        print([coin["symbol"].upper() for coin in data])
        with open("data/fallbackCrypto.py", "w") as f:
            f.write("fallback_crypto = " + repr([coin for coin in data]))
        return [coin for coin in data]

    except Exception as e:
        print("Could not fetch live crypto data. Using fallback.")
        return fallback_crypto
'''
fallback_crypto = [
    "BCH", "XMR", "BSV", "XTZ", "THETA", "ALGO", "FIL", "XLM",
    "ATOM", "EOS", "MKR", "INJ", "QNT", "LDO", "APT", "PEPE",
    "SUI", "KAS", "TAO", "OM", "FTM", "KCS", "WBTC", "WBETH",
    "RETH", "ARBITRUM", "BONK", "SOLANA", "MASQ", "ZEC", "EOS",
    "AAVE", "LINK", "TRU", "STX", "IMX", "STORJ", "CRV", "AXS",
    "GRT", "MANA", "SAND", "ENJ", "CHZ", "XNO", "ZIL", "CAKE",
    "UNI", "COMP", "YFI", "SNX", "LRC", "REN", "BAT", "UMA",
    "CELO", "NEAR", "ADA", "DOT",  "BTC", "ETH", "USDT", "BNB", 
    "SOL", "XRP", "USDC", "ADA", "DOT", "DOGE", "MATIC", "SHIB", 
    "LTC", "AVAX", "WBTC", "LINK", "UNI", "ATOM", "ALGO", "FTT",
    "XLM", "DAI", "VET", "TRX", "ETC", "ICP", "FIL", "HBAR", "NEAR", 
    "EGLD"
]
'''
