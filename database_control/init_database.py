import json
import database_control.database as db


def create_table(cursor, mysql_obj):
    try:
        # 创建表的sql
        sql = "CREATE TABLE IF NOT EXISTS " + mysql_obj["name"] + " ("
        for key, value in mysql_obj.items():
            if key != "name" and key != "备注":
                sql = sql + " " + key + " " + value
        sql += " );"
        cursor.execute(sql)
        db.Loger.logger.info("创建表" + mysql_obj["name"] + "成功")
    except Exception as e:
        db.Loger.logger.info("创建表" + mysql_obj["name"] + "失败")
        db.Loger.logger.error(e)
        db.Loger.logger.exception(e)


def init_create_tables():
    cur = db.connect_mysql()
    # 获取tables
    tables = json.loads(open("config/tables.json", encoding='utf-8').read())
    # 循环遍历表进行创建
    for table in tables:
        create_table(cur[1], table)
    db.close_cursor(cur)
