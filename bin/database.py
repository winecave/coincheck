#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# Database facade program
#
# created  : 2018.01.13
# modified : 2018.--.--
#
# author   : inokuchi koichi
#

import common as com
import psycopg2

# database connection
con = None

def getconnection():
    global con
    try:
        if not con:
            con = psycopg2.connect('host=%s port=%d dbname=%s user=%s' % (
                'localhost', 5432, 'virtcurrency', 'virtadmin'))
            if not con:
                return False
    except Exception as e:
        print(str(e))
        return False

    con.set_session(autocommit=True)

    return con

# ------------------------------------------------------------------------------
# tickers へデータをインサートします
# ------------------------------------------------------------------------------
def insert_tickers(values):
    con = getconnection()

    if not con:
        print('connection error')
        return False

    cur = con.cursor()

    sql = """
        insert into tickers 
            (cur_pair, last, bid, ask, high, low, volume, vol_delta, 
             unixtime, changed_interval, changed, created_at, updated_at)
        values
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now())"""
    try:
        cur.execute(sql, values)
    except Exception as e:
        com.error('insert error -- %s' % str(e))
        return False
    finally:
        cur.close()

    return True
