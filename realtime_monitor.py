import time
import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from bybit_api import BybitAPI
from dotenv import load_dotenv

# Загружаем API ключи и токен Telegram из .env
load_dotenv()
api_key = os.getenv("BYBIT_API_KEY")
api_secret = os.getenv("BYBIT_API_SECRET")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

# Инициализируем API с ключами
api = BybitAPI(api_key, api_secret, testnet=True)


def fetch_latest_data():
    """Получает последние 60 минут цен ETHUSDT и BTCUSDT с интервалом 1 минута."""
    end_time = int(datetime.now().timestamp())
    start_time = end_time - 60 * 60  # 60 минут назад

    eth_data = api.get_historical_data("ETHUSDT", "1", start_time, end_time)
    btc_data = api.get_historical_data("BTCUSDT", "1", start_time, end_time)

    return eth_data, btc_data


def calculate_own_movement(eth_data, btc_data):
    """Определяет собственное движение ETHUSDT, исключая влияние BTCUSDT."""
    eth_df = pd.DataFrame(eth_data)
    btc_df = pd.DataFrame(btc_data)

    eth_changes = eth_df["close"].pct_change().dropna()
    btc_changes = btc_df["close"].pct_change().dropna()

    if len(eth_changes) < 2 or len(btc_changes) < 2:
        return None

    model = LinearRegression()
    X = btc_changes.values.reshape(-1, 1)
    y = eth_changes.values
    model.fit(X, y)

    predicted_eth = model.predict(X)
    residuals = y - predicted_eth

    return pd.Series(residuals, index=eth_changes.index)


def send_telegram_message(message):
    """Отправляет сообщение в Telegram."""
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {"chat_id": telegram_chat_id, "text": message}
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Ошибка отправки сообщения в Telegram: {response.text}")


def monitor_price():
    """Мониторинг изменений цены ETHUSDT и отправка уведомлений при значительных изменениях."""
    print("Начало мониторинга цен ETHUSDT...")

    while True:
        eth_data, btc_data = fetch_latest_data()
        residuals = calculate_own_movement(eth_data, btc_data)

        if residuals is not None and len(residuals) > 1:
            price_change = (
                (residuals.iloc[-1] - residuals.iloc[0]) / abs(residuals.iloc[0]) * 100
            )

            if abs(price_change) >= 1:
                message = f"[{datetime.now()}] Внимание! Собственное изменение цены ETHUSDT: {price_change:.2f}%"
                print(message)
                send_telegram_message(message)

        time.sleep(60)  # Запрос каждые 60 секунд


if __name__ == "__main__":
    monitor_price()
