# - *- coding: utf- 8 - *-
import datetime
import logging
import random
import sqlite3
import time


path_to_db = "botBD.sqlite"


def logger(statement):
    logging.basicConfig(
        level=logging.INFO,
        filename="logs.log",
        format=f"[Executing] [%(asctime)s] | [%(filename)s LINE:%(lineno)d] | {statement}",
        datefmt="%d-%b-%y %H:%M:%S"
    )
    logging.info(statement)


def handle_silently(function):
    def wrapped(*args, **kwargs):
        result = None
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            logger("{}({}, {}) failed with exception {}".format(
                function.__name__, repr(args[1]), repr(kwargs), repr(e)))
        return result

    return wrapped


#######################################################################################################################
# Formatting a request with arguments
def update_format_with_args(sql, parameters: dict):
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)
    return sql, tuple(parameters.values())


# Formatting a request without arguments
def get_format_args(sql, parameters: dict):
    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])
    return sql, tuple(parameters.values())


#######################################################################################################################
########################################### Requests to db ############################################################
def add_user(user_id, username):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO storage_users "
                   "(user_id, username, reg_date) "
                   "VALUES (?, ?, ?)",
                   [user_id, username, get_dates()])
        db.commit()


def update_user(user_id, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"UPDATE storage_users SET XXX WHERE user_id = {user_id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()


def delete_user(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "DELETE FROM storage_users WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()


# Получение пользователя
def get_user(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_users WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchone()
    return get_response


# Получение пользователей
def get_users(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_users WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchall()
    return get_response


# Получение всех пользователей
def get_all_users():
    with sqlite3.connect(path_to_db) as db:
        get_response = db.execute("SELECT * FROM storage_users")
        get_response = get_response.fetchall()
    return get_response


# Получение платежных систем
def get_payment():
    with sqlite3.connect(path_to_db) as db:
        get_response = db.execute("SELECT * FROM storage_payment")
        get_response = get_response.fetchone()
    return get_response


# Изменение платежных систем
def update_payment(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"UPDATE storage_payment SET XXX "
        sql, parameters = update_format_with_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()


# Получение настроек
def get_settings():
    with sqlite3.connect(path_to_db) as db:
        get_response = db.execute("SELECT * FROM storage_settings")
        get_response = get_response.fetchone()
    return get_response


# Обновление настроек
def update_settings(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"UPDATE storage_settings SET XXX "
        sql, parameters = update_format_with_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()


# Добавление пополнения в БД
def add_refill(user_id, user_login, user_name, comment, amount, receipt, way_pay, dates, dates_unix):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO storage_refill "
                   "(user_id, user_login, user_name, comment, amount, receipt, way_pay, dates, dates_unix) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   [user_id, user_login, user_name, comment, amount, receipt, way_pay, dates, dates_unix])
        db.commit()


# Получение пополнения
def get_refill(what_select, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_refill WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchone()
    return get_response


# Получение пополнений
def get_refills(what_select, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_refill WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchall()
    return get_response


# Получение всех пополнений
def get_all_refill():
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_refill"
        get_response = db.execute(sql)
        get_response = get_response.fetchall()
    return get_response


#######################################################################################################################
# Creating all tables
def create_bd():
    with sqlite3.connect(path_to_db) as db:
        # Создание БД с хранением данных пользователей
        check_sql = db.execute("PRAGMA table_info(storage_users)")
        check_sql = check_sql.fetchall()
        check_create_users = [c for c in check_sql]
        if len(check_create_users) == 4:
            print("DB was found(1)")
        else:
            db.execute("CREATE TABLE storage_users("
                       "increment INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "user_id INTEGER, username TEXT, reg_date TIMESTAMP)")
            print("DB was not found(1) | Creating...")

        # Создание БД с хранением данных платежных систем
        check_sql = db.execute("PRAGMA table_info(storage_payment)")
        check_sql = check_sql.fetchall()
        check_create_payment = [c for c in check_sql]
        if len(check_create_payment) == 6:
            print("DB was found(2)")
        else:
            db.execute("CREATE TABLE storage_payment("
                       "qiwi_login TEXT, qiwi_token TEXT, "
                       "qiwi_private_key TEXT, qiwi_nickname TEXT, "
                       "way_payment TEXT, status TEXT)")
            db.execute("INSERT INTO storage_payment("
                       "qiwi_login, qiwi_token, "
                       "qiwi_private_key, qiwi_nickname, "
                       "way_payment, status) "
                       "VALUES (?, ?, ?, ?, ?, ?)",
                       ["None", "None", "None", "None", "form", "False"])
            print("DB was not found(2) | Creating...")

        # Создание БД с хранением настроек
        check_sql = db.execute("PRAGMA table_info(storage_settings)")
        check_sql = check_sql.fetchall()
        check_create_settings = [c for c in check_sql]
        if len(check_create_settings) == 6:
            print("DB was found(3)")
        else:
            db.execute("CREATE TABLE storage_settings("
                       "contact INTEGER, faq TEXT, "
                       "status TEXT, status_buy TEXT,"
                       "profit_buy TEXT, profit_refill TEXT)")
            sql = "INSERT INTO storage_settings(" \
                  "contact, faq, status, status_buy, profit_buy, profit_refill) " \
                  "VALUES (?, ?, ?, ?, ?, ?)"
            now_unix = int(time.time())
            parameters = ("ℹ Контакты. Измените их в настройках бота.\n"
                          "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                          f"Hi",
                          "ℹ Информация. Измените её в настройках бота.\n"
                          "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                          f"Hi",
                          "True", "True", now_unix, now_unix)
            db.execute(sql, parameters)
            print("DB was not found(3) | Creating...")

        # Создание БД с хранением пополнений пользователей
        check_sql = db.execute("PRAGMA table_info(storage_refill)")
        check_sql = check_sql.fetchall()
        check_create_refill = [c for c in check_sql]
        if len(check_create_refill) == 10:
            print("DB was found(4/4)")
        else:
            db.execute("CREATE TABLE storage_refill("
                       "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "user_id INTEGER, user_login TEXT, "
                       "user_name TEXT, comment TEXT, "
                       "amount TEXT, receipt TEXT, "
                       "way_pay TEXT, dates TIMESTAMP, "
                       "dates_unix TEXT)")
            print("DB was not found(4) | Creating...")
