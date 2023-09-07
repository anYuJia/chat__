import json
import logging
import sys

import pymysql

global con


class Loger:
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.INFO)
    file1logger = logging.getLogger()
    file1logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("./log/log.log")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('time:%(asctime)s  - %(levelname)s-line:%(lineno)s - %(message)s')
    handler.setFormatter(formatter)
    rf_handler = logging.StreamHandler(sys.stderr)  # 默认是sys.stderr
    rf_handler.setLevel(logging.DEBUG)
    # rf_handler = logging.handlers.TimedRotatingFileHandler('all.log', when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
    rf_handler.setFormatter(logging.Formatter("time:%(asctime)s  - %(levelname)s-line:%(lineno)s - %(message)s"))
    logger.addHandler(handler)
    logger.addHandler(rf_handler)


# 连接数据库
def connect_mysql():
    f = open("./config/mysql_config.json", "r")
    ff = f.read()
    config = json.loads(ff)["MysqlInfo"]
    # 创建连接
    conn = pymysql.connect(host=config["host"], port=config["port"], user=config["user"], password=config["password"],
                           db=config["db"], charset=config["charset"])
    # 返回游标(查询数据返回为元组格式)
    Db = [conn, conn.cursor()]
    return Db


# 获取数据库句柄
def getDb():
    return con


# 断开数据库连接
def close_cursor(cursor):
    cursor[0].close()
    cursor[1].close()
