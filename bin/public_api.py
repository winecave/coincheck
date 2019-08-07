# -*- coding: utf-8 -*-
#
# Coincheck public apis
#
# created: 2018.01.10
# author : k.inokuchi
#

import common as com
import traceback
import requests
from datetime import datetime

# API サーバ名
API_SERVER = 'coincheck.com'

# デフォルト通貨ペア
DEFAULT_PAIR = 'btc_jpy'

APIS = {
  'ticker': {'url': '/api/ticker', 'request_type': 'GET'},
  'trades': {'url': '/api/trades', 'request_type': 'GET'},
  'order_books': {'url': '/api/order_books', 'request_type': 'GET'},
  'order_rate' : {'url': '/api/exchange/orders/rate', 'request_type': 'GET'},
  'rate'  : {'url': '/api/rate/', 'request_type': 'GET'}}
# ------------------------------------------------------------------------------
# requests wrapper method
# リクエストが成功するとJSON オブジェクトを返します
# ------------------------------------------------------------------------------
def get(url, params=None):
    try:
        t0 = datetime.now()
        if params and 'pair' in params.keys():
            com.debug('---------- currency pair : {0}'.format(params['pair']))
        com.debug('{0} executed'.format(url))
        r = requests.get(url, params)
        if r.status_code == 200:
            com.debug('200 OK response: {0}'.format(r.text))
            return r.json()
        else:
            com.warn('status code : {0:d}'.format(r.status_code))
            return False
    except Exception as e:
        com.error(str(e))
        com.error(traceback.format_exc())
        return False
    finally:
        t1 = datetime.now()
        delta = t1 - t0
        com.info('get {0} exec time : {1:d}.{2:06d}'.format(url, delta.seconds, delta.microseconds))
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# 各種最新情報を返します
# -- Response from https://API_SERVER/api/ticker sample --
# {
#   "last": 27390,              # 最後の取引の価格
#   "bid": 26900,               # 現在の買い注文の最高価格
#   "ask": 27390,               # 現在の売り注文の最安価格
#   "high": 27659,              # 24時間での最高取引価格
#   "low": 26400,               # 24時間での最安取引価格
#   "volume": "50.29627103",    # 24時間での取引量
#   "timestamp": 1423377841     # 現在の時刻
# }
# ------------------------------------------------------------------------------
def get_ticker(pair=DEFAULT_PAIR):
    return get('https://{0}/api/ticker'.format(API_SERVER), \
               {'pair': pair})
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# 板情報を返します
# -- Response from https://API_SERVER/api/order_books sample --
# {
#   "asks": [
#     [27330, "2.25"],    # レート、注文量の並び順
#     [27340, "0.45"]],
#   "bids": [
#     [27240, "1.1543"],
#     [26800, "1.2226"]]
# }
# ------------------------------------------------------------------------------
def get_order_books(pair=DEFAULT_PAIR):
    return get('https://{0}/api/order_books'.format(API_SERVER), \
               {'pair': pair})
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
#
# 注文をもとにレートを返します
# -- Request Parameters --
#  order_type 注文のタイプ（"sell" or "buy"）
#  pair 取引ペア。現在は "btc_jpy" のみです。
#  amount 注文での量。（例）0.1
#  price 注文での金額。（例）28000
#
# -- Response from https://API_SERVER/api/exchange/orders/rate sample --
# {
#   "success": true,
#   "rate": 60000,
#   "price": 60000,
#   "amount": 1
# }
# ------------------------------------------------------------------------------
def get_rate(type, pair=DEFAULT_PAIR):
    return get('https://{0}/api/exchange/orders/rate'.format(API_SERVER), \
               {'order_type': type, 'pair': pair, 'amount': 1})
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# 売り注文レート取得 
# ------------------------------------------------------------------------------
def get_sell_rate(pair=DEFAULT_PAIR):
    return get_rate('sell', pair)
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# 買い注文レート取得
# ------------------------------------------------------------------------------
def get_buy_rate(pair=DEFAULT_PAIR):
    return get_rate('buy', pair)
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# 指定通貨ペアの販売レートを返します
# ------------------------------------------------------------------------------
def get_hanbai_rate(pair=DEFAULT_PAIR):
    return get('https://{0}/api/rate/{1}'.format(API_SERVER, pair))
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# 全取引履歴を返します
# 履歴は降順、最大50履歴固定で返します
# ------------------------------------------------------------------------------
def get_trade_history(pair=DEFAULT_PAIR):
    return get('https://{0}/api/trades'.format(API_SERVER), \
               {'limit': 50, 'order': 'desc', 'pair': pair})
# ------------------------------------------------------------------------------


if __name__ == '__main__':
    import time
    t0 = time.time()
    obj = get_ticker()
    print(obj)
    print(obj['last'])
    print(obj['bid'])
    print(obj['ask'])
    print(obj['high'])
    print(obj['low'])
    print(obj['volume'])
    print(obj['timestamp'])
    t1 = time.time()
    delta = t1 - t0
    print('{0:8f}'.format(delta))
