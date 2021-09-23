import json

from flask import Flask, render_template, request, flash, redirect, jsonify
import config
from binance.client import Client
from binance.enums import *

app = Flask(__name__)
app.secret_key = b'somelongrandomstring'
client = Client(config.API_KEY,config.API_SECRET)


# if __name__ == '__main__':
#     app.debug = True  # 開啟debug 模式
#     app.run()


@app.route("/")
def index():
    title = '幣安交易系統'
    account = client.get_account()
    balances = account['balances']
    symbol_list = sort_symbol()
    often_use = often_use_list()
    return render_template('index.html', title=title, my_balances=balances, symbols=symbol_list, often_list=often_use)


def often_use_list():
    symbol_list = []
    symbol_list.append(client.get_symbol_info("BTCUSDC"))
    symbol_list.append(client.get_symbol_info("ETHUSDC"))
    symbol_list.append(client.get_symbol_info("BNBUSDC"))
    return symbol_list


def sort_symbol():
    exchange_info = client.get_exchange_info()
    exchange_info_list = exchange_info['symbols']
    exchange_info_list = sorted(exchange_info_list, reverse=False, key=str)
    return exchange_info_list
    # 印出 symbol 所有項目
    # for symbol_info in exchange_info_list:
    #     print(symbol_info['symbol'])


@app.route('/buy', methods=['POST'])
def buy():
    print(request.form)
    try:
        order = client.create_order(symbol=request.form['symbol'],
                                    side=SIDE_BUY,
                                    type=ORDER_TYPE_MARKET,
                                    quantity=request.form['quantity_buy'])
    except Exception as e:
        flash(e.message, "error")

    return redirect('/')


@app.route('/sell', methods=['POST'])
def sell():
    print(request.form)
    try:
        order = client.create_order(symbol=request.form['symbol'],
                                    side=SIDE_SELL,
                                    type=ORDER_TYPE_MARKET,
                                    quantity=request.form['quantity_sell'])
    except Exception as b:
        flash(b.message, "error")

    return redirect('/')


@app.route('/settings')
def settings():
    return '設定'


@app.route('/history')
def history():
    candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 Jul, 2021",
                                                "14 Aug, 2021")

    processed_candlesticks = []

    for data in candlesticks:
        candlestick = {
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4]
        }

        processed_candlesticks.append(candlestick)

    return jsonify(processed_candlesticks)