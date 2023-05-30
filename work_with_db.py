import sqlite3 as sl

import gspread as gspread


def get_last():
    conn = sl.connect('db.db')
    with conn:
        return conn.execute("SELECT date, count FROM work ORDER BY id DESC LIMIT 10;").fetchall()


def get_today_count():
    conn = sl.connect('db.db')
    with conn:
        return conn.execute("SELECT count FROM work WHERE date = DATE('now', 'localtime');").fetchone()


def get_or_create_today():
    conn = sl.connect('db.db')
    today_count = get_today_count()
    if today_count:
        return str(*today_count)
    else:
        with conn:
            conn.execute("INSERT INTO work(date, count) VALUES(DATE('now', 'localtime'), 0);")
        return "0"


def increase_count(count):
    conn = sl.connect('db.db')
    with conn:
        conn.execute(f"UPDATE work SET count = {count} WHERE date = DATE('now', 'localtime');")


def export_to_google():
    gc = gspread.service_account(filename='key.json')
    sh = gc.open("HamsterApp")
    worksheet = sh.sheet1
    last = int(worksheet.acell('C1').value)
    last_date = str(worksheet.acell(f'A{last}').value)
    conn = sl.connect('db.db')
    with conn:
        days = conn.execute(f"SELECT date, count FROM work WHERE date > '{last_date}';").fetchall()
    print(last, last_date, days)
    for day in days:
        worksheet.update_cell(last + 1, 1, day[0])
        worksheet.update_cell(last + 1, 2, day[1])

def reset_today():
    conn = sl.connect('db.db')
    with conn:
        conn.execute(f"UPDATE work SET count = 0 WHERE date = DATE('now', 'localtime');")
# conn = sl.connect('db.db')
# conn.execute(f"CREATE TABLE work("
#              f"id INTEGER PRIMARY KEY,"
#              f"date DATETIME NOT NULL,"
#              f"count INTEGER NOT NULL);")
