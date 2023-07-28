import logging
from binance.um_futures import UMFutures
from binance.lib.utils import config_logging

config_logging(logging, logging.INFO)


class Binance():
    def __init__(self):
        self.client = UMFutures()

    def __get_symbols__(self):
        symbols = self.client.exchange_info()

        filtered_symbols = []
        for symbol_info in symbols['symbols']:
            if symbol_info['status'] == 'TRADING' and symbol_info['quoteAsset'] == 'USDT':
                filtered_symbols.append(symbol_info['symbol'])

        return sorted(filtered_symbols)

    def get_result(self, dias):
        symbols = self.__get_symbols__()
        interval = '1d'

        result = []
        for symbol in symbols:
            klines = self.client.klines(
                symbol=symbol, interval=interval, limit=dias)
            nKlines = len(klines) - 1
            old_close = float(klines[0][4])
            new_close = float(klines[nKlines][4])
            percent = round((new_close - old_close) / old_close * 100, 2)
            item = {'symbol': symbol, 'old': old_close,
                    'new': new_close, 'percent': percent}
            result.append(item)

        # Filtra los mayores y menores a cero
        negativos = [item for item in result if item['percent'] < 0]
        positivos = [item for item in result if item['percent'] > 0]

        # Los ordena por el porcentaje
        negativos_sorted = sorted(negativos, key=lambda x: x['percent'])
        positivos_sorted = sorted(
            positivos, key=lambda x: x['percent'], reverse=True)

        return negativos_sorted, positivos_sorted
