import pandas as pd
from bybit_api import BybitAPI
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression


def get_price_changes(data):
    """Получает изменения цены из списка свечей."""
    df = pd.DataFrame(data)
    df['close'] = df['close'].astype(float)
    df['price_change'] = df['close'].pct_change()
    return df['price_change'].dropna()


def calculate_correlation(eth_changes, btc_changes):
    """Вычисляет корреляцию между изменениями цены ETHUSDT и BTCUSDT."""
    return eth_changes.corr(btc_changes)


def calculate_residuals(eth_changes, btc_changes):
    """Вычисляет остатки регрессии для ETHUSDT, очищенные от влияния BTCUSDT."""
    # Преобразуем данные в нужный формат для регрессии
    X = btc_changes.values.reshape(-1, 1)  # BTCUSDT как независимая переменная
    y = eth_changes.values  # ETHUSDT как зависимая переменная

    # Настраиваем линейную регрессию
    model = LinearRegression()
    model.fit(X, y)

    # Предсказываем влияние BTCUSDT на ETHUSDT
    predicted_eth = model.predict(X)

    # Получаем остатки регрессии
    residuals = y - predicted_eth
    return residuals


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

    # Вычисляем остатки регрессии
    residuals = calculate_residuals(eth_changes, btc_changes)
    print("Остатки регрессии (движение ETHUSDT, очищенное от влияния BTCUSDT):")
    print(residuals)
