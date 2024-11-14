import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode

class BybitAPI:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api-testnet.bybit.com" if testnet else "https://api.bybit.com"
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def get_historical_data(self, symbol: str, interval: str, start_time: int, end_time: int):
        """Получает исторические данные свечей с использованием актуального эндпоинта V5."""
        endpoint = "/v5/market/kline"
        url = self.base_url + endpoint

        params = {
            "category": "linear",
            "symbol": symbol,
            "interval": interval,
            "start": start_time * 1000,  # Время в миллисекундах
            "end": end_time * 1000,      # Время в миллисекундах
            "api_key": self.api_key,
            "timestamp": str(int(time.time() * 1000)),
        }

        query_string = urlencode(sorted(params.items()))
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        params["sign"] = signature

        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Извлекаем данные из 'list'
        if "result" in data and "list" in data["result"]:
            candles = data["result"]["list"]
            # Преобразуем в формат, ожидаемый остальной программой
            formatted_data = [
                {
                    "timestamp": int(candle[0]),
                    "open": float(candle[1]),
                    "high": float(candle[2]),
                    "low": float(candle[3]),
                    "close": float(candle[4]),
                    "volume": float(candle[5]),
                    "turnover": float(candle[6])
                }
                for candle in candles
            ]
            return formatted_data
        else:
            print("Ошибка: Ожидаемого поля 'list' нет в ответе.")
            print("Ответ:", data)
            return []
