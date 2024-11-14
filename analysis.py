import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from bybit_api import BybitAPI
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Подключаемся к тестовой среде с ключами
# Получаем API ключи из переменных окружения
api_key = os.getenv("BYBIT_API_KEY")
api_secret = os.getenv("BYBIT_API_SECRET")

# Инициализируем API с ключами
api = BybitAPI(api_key, api_secret, testnet=True)


def get_price_changes(data):
    """Получает изменения цены из списка свечей."""
    if not data:
        raise ValueError("Нет данных для анализа")
    df = pd.DataFrame(data)
    if "close" not in df.columns:
        raise KeyError("'close' column is missing in the data.")
    df["close"] = df["close"].astype(float)
    df["price_change"] = df["close"].pct_change()
    return df["price_change"].dropna()


def calculate_correlation(eth_changes, btc_changes):
    return eth_changes.corr(btc_changes)


def calculate_residuals(eth_changes, btc_changes):
    X = btc_changes.values.reshape(-1, 1)
    y = eth_changes.values
    model = LinearRegression()
    model.fit(X, y)
    predicted_eth = model.predict(X)
    residuals = y - predicted_eth
    return pd.Series(residuals, index=eth_changes.index)


def plot_changes(eth_changes, btc_changes, residuals):
    plt.figure(figsize=(14, 7))
    plt.subplot(2, 1, 1)
    plt.plot(eth_changes.index, eth_changes, label="ETHUSDT Changes", color="blue")
    plt.plot(btc_changes.index, btc_changes, label="BTCUSDT Changes", color="orange")
    plt.title("Изменения ETHUSDT и BTCUSDT")
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(residuals.index, residuals, label="ETHUSDT Residuals", color="green")
    plt.title("Очищенные остатки ETHUSDT (без влияния BTCUSDT)")
    plt.legend()
    plt.tight_layout()
    plt.show()


def fetch_data_in_chunks(api, symbol, interval, start_time, end_time, chunk_hours=6):
    """Запрашивает данные кусками, чтобы избежать перегрузки API."""
    data = []
    chunk_seconds = chunk_hours * 3600
    current_time = start_time
    while current_time < end_time:
        next_time = min(current_time + chunk_seconds, end_time)
        try:
            chunk_data = api.get_historical_data(
                symbol, interval, current_time, next_time
            )
            if not chunk_data:
                print(
                    f"Пустой ответ от API для символа {symbol} в интервале с {current_time} по {next_time}."
                )
            else:
                print(
                    f"Получены данные для символа {symbol}: {chunk_data[:2]}..."
                )  # Показываем первые две записи
            data.extend(chunk_data)
            current_time = next_time
        except Exception as e:
            print(f"Ошибка при запросе данных: {e}")
            break
    return data


# Основной код для анализа
if __name__ == "__main__":
    now = int(datetime.now().timestamp())
    one_day_ago = int((datetime.now() - timedelta(days=1)).timestamp())

    # Запрашиваем данные по частям
    eth_data = fetch_data_in_chunks(api, "ETHUSDT", "60", one_day_ago, now)
    btc_data = fetch_data_in_chunks(api, "BTCUSDT", "60", one_day_ago, now)

    if eth_data and btc_data:
        eth_changes = get_price_changes(eth_data)
        btc_changes = get_price_changes(btc_data)

        correlation = calculate_correlation(eth_changes, btc_changes)
        print(f"Корреляция между ETHUSDT и BTCUSDT: {correlation}")

        residuals = calculate_residuals(eth_changes, btc_changes)
        print("Остатки регрессии (движение ETHUSDT, очищенное от влияния BTCUSDT):")
        print(residuals)

        plot_changes(eth_changes, btc_changes, residuals)
    else:
        print("Недостаточно данных для анализа.")
