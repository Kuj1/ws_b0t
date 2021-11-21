import sqlite3
import aiogram
try:
    conn = sqlite3.connect('data/olx.db')
    print('[INFO]: БД подключена')
    # sql_create_table_query = '''CREATE TABLE item_olx (
    #                             item_photo TEXT,
    #                             item_city TEXT,
    #                             item_title TEXT,
    #                             item_price TEXT,
    #                             item_url TEXT);'''
    sql_show_query = '''SELECT * FROM item_olx'''

    cursor = conn.cursor()
    # cursor.execute(sql_create_table_query)
    # print('[INFO]: БД создана')
    cursor.execute(sql_show_query)

    result = cursor.fetchall()

    for i in result:
        print(f'\nitem_photo: {i[0]} \nitem_city: {i[1]} \nitem_title: {i[2]} \nitem_price: {i[3]} '
              f'\nitem_url: {i[4]}')

    conn.cursor()

    conn.close()
    print('\n[INFO]: БД отключена')
except sqlite3.Error as error:
    print(f'[ERROR]: Ошибка при подключении к БД \n{error}')