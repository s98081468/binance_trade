import time
import logging
#追蹤有什麼事件發生的動作稱為 Logging
from utils import config
from trader.binance_spot_trader import BinanceSpotTrader
from trader.binance_future_trader import BinanceFutureTrader

#應該是logging用法
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=format, filename='log.txt')
logger = logging.getLogger('binance')

if __name__ == '__main__':


    config.loads('./config.json')
#合約與現貨切換
    if config.platform == 'binance_spot':
        trader = BinanceSpotTrader()
    else:
        trader = BinanceFutureTrader()
 
    orders = trader.http_client.cancel_open_orders(config.symbol)
    print(f"cancel orders: {orders}")

    while True:
        try:
            trader.start()
            time.sleep(20)
        
        except Exception as error:
            print(f"catch error: {error}")
            time.sleep(5)