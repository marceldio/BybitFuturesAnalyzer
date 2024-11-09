import pandas as pd
from bybit_api import BybitAPI
from datetime import datetime, timedelta


def get_price_changes(data):
    """Получает изменения цены из списка свечей."""
    df = pd.DataFrame(data)
    df['close'] = df['close'].astype(float)
    # Рассчитываем процентное изменение цены закрытия
    df['price_change'] = df['close'].pct_change()
    return df['price_change']


def calculate_correlation(eth_changes, btc_changes):
    """Вычисляет корреляцию между изменениями цены ETHUSDT и BTCUSDT."""
    correlation = eth_changes.corr(btc_changes)
    return correlation


# Основной код для анализа
if __name__ == "__main__":
    api = BybitAPI()

    # Получаем данные за последний день
    now = int(datetime.now().timestamp())
    one_day_ago = int((datetime.now() - timedelta(days=1)).timestamp())

    eth_data = api.get_historical_data("ETHUSDT", "60", one_day_ago, now)
    btc_data = api.get_historical_data("BTCUSDT", "60", one_day_ago, now)

    # Получаем изменения цены
    eth_changes = get_price_changes(eth_data)
    btc_changes = get_price_changes(btc_data)

    # Вычисляем корреляцию
    correlation = calculate_correlation(eth_changes, btc_changes)
    print(f"Корреляция между ETHUSDT и BTCUSDT: {correlation}")
