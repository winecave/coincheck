#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# Ticker logging program
#
# created  : 2018.01.13
# modified : 2018.--.--
#
# author   : inokuchi koichi
#

import common     as com
import database   as db
import datetime   as dt
import public_api as pub_api
import sys
from os      import getpid, uname
from os.path import abspath
from time    import sleep
from time    import time

class ticker:
    def __init__(self, cur_pair, obj):
        self.cur_pair = cur_pair
        self.last = obj['last']
        self.bid  = obj['bid']
        self.ask  = obj['ask']
        self.high = obj['high']
        self.low  = obj['low']
        self.volume   = obj['volume']
        self.unixtime = obj['timestamp']

# 直近のticker
last_ticker = None

def collect(pair='btc_jpy'):
    obj = pub_api.get_ticker(pair)

    # ラムダ式定義（現在値と直近値の大小を計算する簡易な比較関数）
    isstay   = lambda now, prev: now == prev
    ishigher = lambda now, prev: now > prev
 
    if obj:
        global last_ticker
        # 変更間隔計算
        changed_interval = obj['timestamp'] - last_ticker.unixtime
        # 取引volume差分計算
        vol_delta = obj['volume'] - last_ticker.volume
        # 変更ありフラグ初期化
        changed = 0
        # last変動のchange weight計算
        if isstay(obj['last'], last_ticker.last):
            changed += 2
        elif ishigher(obj['last'], last_ticker.last):
            changed += 4

        # low変動のchange weight計算
        if isstay(obj['low'], last_ticker.low):
            changed += 16
        elif ishigher(obj['low'], last_ticker.low):
            changed += 32
        else:
            changed += 8

        # highw変動のchange weight計算
        if isstay(obj['high'], last_ticker.high):
            changed += 128
        elif ishigher(obj['high'], last_ticker.high):
            changed += 256
        else:
            changed += 64

        if changed_interval:
            last_ticker = ticker(pair, obj)

        if not db.insert_tickers(
            [pair,
             obj['last'],
             obj['bid'],
             obj['ask'],
             obj['high'],
             obj['low'],
             obj['volume'],
             vol_delta,
             obj['timestamp'],
             changed_interval,
             changed]):
            com.error('ticker insert error')

if __name__ == '__main__':
    with open('/root/dev/bin/ticker_logger.pid', 'w') as f:
        f.write('{0:d}'.format(getpid()))
    com.info('ticker logger started !')
    com.info('  Python version : {0}'.format(str(sys.version_info)))
    com.info('  Program File   : {0}'.format(abspath(__file__)))
    com.info('  Hostname       : {0}'.format(uname()[1]))

    # デフォルト通貨ペア設定
    pair = 'btc_jpy'

    obj = pub_api.get_ticker(pair)

    if obj:
        last_ticker = ticker(pair, obj)

    while True:
        sleep(1)
        collect(pair)
