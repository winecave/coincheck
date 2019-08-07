# -*- coding: utf-8 -*-
#
# created: 2018.01.10
# author : k.inokuchi
#

from datetime import datetime
from json     import load
from os       import getenv
from os.path  import abspath
from os.path  import basename
from os.path  import dirname
from os.path  import exists
from sys      import argv

LOG_LEVEL = {0: 'fine', 1: 'debug', 2:'info', 3: 'warn', 4: 'error'}
LOG_FINE = 0
LOG_DEBUG = 1
LOG_INFO = 2
LOG_WARN = 3
LOG_ERROR = 4

# ------------------------------------------------------------------------------
# プログラムホームを返します
# ------------------------------------------------------------------------------
def get_home():
    return dirname(dirname(abspath(argv[0])))


# ------------------------------------------------------------------------------
# ログファイルのパスを返します
# ------------------------------------------------------------------------------
def get_logpath():
    return '{0}/log/{1}.log'.format(get_home(), basename(argv[0])[:-3])


# ------------------------------------------------------------------------------
# /APP_HOME/conf/conf.json の読み込み結果をJSONオブジェクトとして返します
# ------------------------------------------------------------------------------
def get_config():
    conf_path = '{0}/conf/conf.json'.format(get_home())
    with open(conf_path) as f:
        obj = load(f)
    return obj


# ------------------------------------------------------------------------------
# 現在のログレベルを返します
# ------------------------------------------------------------------------------
def get_loglevel():
    log_level_file = '{0}/bin/LOG_LEVEL'.format(get_home())
    if exists(log_level_file):
        with open(log_level_file) as f:
            level = f.read()
            level = int(level.replace('\n', ''))
    else:
        level = getenv('LOG_LEVEL', 2)
    return level

# ------------------------------------------------------------------------------
# ログを出力します。
# ------------------------------------------------------------------------------
def putLog(level, message):
    if level < get_loglevel():
        return
    with open(get_logpath(), 'a') as f:
        f.write('{0:s} [{1:s}] {2:s}\n'.format( \
            datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            LOG_LEVEL[level],
            message))

def fine(message):
    putLog(LOG_FINE, message)

def debug(message):
    putLog(LOG_DEBUG, message)

def info(message):
    putLog(LOG_INFO, message)

def warn(message):
    putLog(LOG_WARN, message)

def error(message):
    putLog(LOG_ERROR, message)

if __name__ == '__main__':
    print(get_home())
    print(get_config())
    print(get_logpath())
    print(get_loglevel())
    fine('Thisis is fine message.')
    debug('Thisis is debug message.')
    info('Thisis is info message.')
    warn('Thisis is warn message.')
    error('Thisis is error message.')
