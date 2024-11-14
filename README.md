# BybitFuturesAnalyzer
Приложение для анализа цен фьючерса

1. Определить собственные движения цены фьючерса ETHUSDT, 
исключив из них движения, вызванные влиянием цены BTCUSDT.
  
2. Написать программу которая в реальном времени (с минимальной задержкой)
следит за ценой фьючерса ETHUSDT и определяет собственные движения цены ETH.
При изменении цены на 1% за последние 60 минут, программа выводит сообщения
в консоль. Программа должна продолжать работать дальше, постоянно считывая
актуальную цену.

3. Дополнительно: Создал тг-бота при изменении цены ETHUSDT более чем на 1% 
за последние 60 минут бот отправляет уведомления в Telegram.

Методика исключения влияния:
Для исключения влияния цены BTCUSDT на движение ETHUSDT буду использовать 
подход на основе анализа корреляции и регрессии. 

Шаг 1: Сбор данных
Соберу исторические данные по ценам фьючерсов ETHUSDT и BTCUSDT. 
С Bybit API можно запрашивать данные в заданном временном диапазоне и интервале (например, минутные или часовые свечи).

Шаг 2: Определение корреляции
Рассчитаю корреляцию между изменениями цены BTCUSDT и ETHUSDT на каждом временном интервале. 
Высокий уровень корреляции подскажет, что движения цен ETHUSDT зависят от BTCUSDT.
Изменения цены можно измерить, используя процентное изменение (pct_change()) или разницу в закрытиях.

Шаг 3: Регрессионный анализ
Используем линейную регрессию для моделирования влияния BTCUSDT на ETHUSDT:
BTCUSDT будет независимой переменной (X), ETHUSDT — зависимой (y).
На основе этой модели мы сможем предсказать «зависимую» часть движения ETHUSDT, вызванную BTCUSDT.

Шаг 4: Исключение влияния BTCUSDT
Получим остаток регрессии (разницу между фактической ценой ETHUSDT и предсказанной моделью).
Эти «остатки» представляют движение ETHUSDT, очищенное от влияния BTCUSDT, 
и их можно использовать для дальнейшего анализа или поиска аномалий.

Шаг 5: Подбор параметров
Параметры для подбора:
Временной интервал (5 минут, 1 час и т.д.)
Количество данных для определения зависимости (например, последние 1000 свечей)
Порог значимости корреляции для анализа (например, корреляция выше 0.5 может считаться значительной).
