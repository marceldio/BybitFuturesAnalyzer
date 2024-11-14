import requests
import os
import time
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем API ключи из переменных окружения
api_key = os.getenv("BYBIT_API_KEY")
api_secret = os.getenv("BYBIT_API_SECRET")


def get_wallet_balance():
    """Получает баланс кошелька с использованием Bybit V5 API."""
    base_url = "https://api-testnet.bybit.com"
    endpoint = "/v5/account/wallet-balance"
    url = base_url + endpoint

    # Параметры запроса
    params = {
        "api_key": api_key,
        "timestamp": str(int(time.time() * 1000)),
        "accountType": "UNIFIED",  # или другой тип аккаунта, если используется
    }

    # Сортируем параметры и создаем строку для подписи
    sorted_params = dict(sorted(params.items()))
    query_string = urlencode(sorted_params)

    # Создаем подпись
    signature = hmac.new(
        api_secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    # Добавляем подпись к параметрам
    params["sign"] = signature

    try:
        # Отправляем GET-запрос с параметрами
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверяем успешность запроса

        data = response.json()
        if "result" in data:
            print("Аутентифицированное подключение успешно. Получены данные:")
            print(data["result"])
        else:
            print("Ошибка: Ожидаемого поля 'result' нет в ответе.")
            print("Ответ:", data)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err}")
    except Exception as err:
        print(f"Другая ошибка: {err}")


if __name__ == "__main__":
    get_wallet_balance()
