from auth.connectClient import newsClient
from alpaca.data.requests import NewsRequest
from datetime import datetime, timedelta

class NewsBot:
    def __init__(self):
        pass

    def get_latest_news(self, symbol, limit=1):
        try:
            request = NewsRequest(
            symbols=symbol,
            start=datetime.now() - timedelta(days=1),
            end=datetime.now(),
            limit=limit
            )
            news_set = newsClient.get_news(request)
            #print(news_set['news'][0].headline)
            headline = news_set['news'][0].headline or ''
            summary = news_set['news'][0].summary or ''
        
            return {"headline": headline, "summary": summary}

        except Exception as e:
            print(f"News fetch failed for {symbol}: {e}")

        return {"headline": None, "summary": None}
