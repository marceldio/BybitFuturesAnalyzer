import requests
import os
from datetime import datetime, timedelta


class BybitAPI:
    def __init__(self):
        self.base_url = "https://api.bybit.com"
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def get_historical_data(self, symbol: str, interval: str, start_time: int, end_time: int):
        """Получает исторические данные свечей."""
        endpoint = "/v2/public/kline/list"
        params = {
            "symbol": symbol,
            "interval": interval,
            "from": start_time,
            "to": end_time
        }
        response = self.session.get(self.base_url + endpoint, params=params)
        response.raise_for_status()
        return response.json().get("result", [])


if __name__ == "__main__":
    api = BybitAPI()

    # Получим данные за последний день для пары ETHUSDT с интервалом 1 час
    now = int(datetime.now().timestamp())
    one_day_ago = int((datetime.now() - timedelta(days=1)).timestamp())

    eth_data = api.get_historical_data("ETHUSDT", "60", one_day_ago, now)
    btc_data = api.get_historical_data("BTCUSDT", "60", one_day_ago, now)

    print("ETHUSDT Data:", eth_data)
    print("BTCUSDT Data:", btc_data)
