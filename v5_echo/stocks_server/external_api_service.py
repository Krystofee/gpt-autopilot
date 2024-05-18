import requests
from config import API_KEY

API_URL = "https://www.alphavantage.co/query"


def fetch_intraday_data(symbol: str, interval: str = '5min') -> dict:
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': interval,
        'apikey': API_KEY
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()  # Raise an error for bad status codes
    data = response.json()
    return data.get('Time Series (5min)', {})
