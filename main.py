from tvDatafeed import TvDatafeed, Interval
import asyncio
import numpy as np


async def getETHhourChange():
    tv = TvDatafeed() # Библиотека для парсинга с TradingView. Без авторизации вроде есть ограничения по частоте запросов
    while True:
        priceBTC = []
        priceETH = []

        # Спот btc/usdt. Берём 60 последних свечей по минуте
        dataBTC = tv.get_hist('BTCUSDT', 'BINANCE', interval=Interval.in_1_minute, n_bars=60)['open']
        # Фьючерсный eth/usdt, тут правда только последний месяц учитывается, но нам больше и не надо
        dataETH = tv.get_hist('ETHUSDT30M2023', 'BINANCE', interval=Interval.in_1_minute, n_bars=60)['open']

        # Наполняем массивы ценами
        for i in range(60):
            priceBTC.append(dataBTC[i])
            priceETH.append(dataETH[i])

        # Ищем корреляцию
        corr = np.corrcoef(priceBTC, priceETH)[0, 1]

        # Высчитываем изменение цены ETH, исключая давление BTC, по крайней мере, я так думаю. Если корреляция нулевая,
        # то всё изменение цены ETH считается собственным.
        change =((priceETH[-1] / priceETH[0])-1)*(1-corr)

        # Сообщение при изменении на 1% собственных движений eth за последний час
        if change >= 0.01:
            print(f'Цена eth изменилась на {((change*100)//0.01)/100}%')
            await asyncio.sleep(60) # ждём следующую минуту, пока изменений не будет




def main():
    el = asyncio.get_event_loop()
    el.run_until_complete(getETHhourChange())
    el.close()

if __name__ == "__main__":
    main()
