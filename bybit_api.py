import requests
import time
import os


class BybitAPI:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api-testnet.bybit.com" if testnet else "https://api.bybit.com"
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def get_historical_data(self, symbol: str, interval: str, start_time: int, end_time: int, max_retries: int = 5):
        """Получает исторические данные свечей с поддержкой API-ключей и измененной базовой URL."""
        endpoint = "/v2/public/kline/list"
        params = {
            "symbol": symbol,
            "interval": interval,
            "from": start_time,
            "to": end_time,
            "api_key": self.api_key,
            # Добавим другие параметры аутентификации, если требуется
        }

        retries = 0
        while retries < max_retries:
            response = self.session.get(self.base_url + endpoint, params=params)
            if response.status_code == 429:
                wait_time = 2 ** retries
                print(f"Ошибка 429: Превышен лимит запросов. Повтор через {wait_time} секунд...")
                time.sleep(wait_time)
                retries += 1
            else:
                response.raise_for_status()
                return response.json().get("result", [])

        raise Exception("Превышено количество попыток при запросе данных с Bybit API")
