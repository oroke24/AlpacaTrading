import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
class ScraperBot:
    def __init__(self):
        pass

    def make_request(self, url, retries=3, delay=1):
        for i in range(retries):
            try:
                return requests.get(url, headers=HEADERS, timeout=10)
            except requests.RequestException as e:
                if i == retries - 1: raise
                time.sleep(delay)

    def get_top_gainers_yahoo(self):
        url = "https://finance.yahoo.com/gainers"
        soup = BeautifulSoup(self.make_request(url).text, "html.parser")
        rows = soup.select("table tbody tr")

        return [
            {
                'symbol': cells[0].text.strip(),
                'company': cells[1].text.strip()
            }
            for row in rows
            if (cells := row.find_all("td")) and len(cells) >= 2
        ]



