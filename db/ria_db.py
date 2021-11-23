import sqlite3
import os


def sql_connect_to_ria():
    if os.path.exists('db_archive/'):
        pass
    else:
        os.mkdir('db_archive/')
    ria_db = sqlite3.connect('db_archive/ria_db')
    cursor = ria_db.cursor()
    if ria_db:
        print('[INFO]: Database is connected')
    ria_db.execute("""CREATE TABLE IF NOT EXISTS ria_links(link TEXT UNIQUE)""")
    ria_db.commit()


async def sql_add_link_to_ria(state):
    ria_db = sqlite3.connect('db_archive/ria_db')
    cursor = ria_db.cursor()

    async with state.proxy() as url:
        cursor.execute("""INSERT OR IGNORE INTO ria_links VALUES(?)""", tuple(url.values()))
        ria_db.commit()


async def sql_read_ria_link():
    ria_db = sqlite3.connect('db_archive/ria_db')
    cursor = ria_db.cursor()

    return cursor.execute("""SELECT * FROM ria_links""").fetchall()


async def sql_remove_ria_link():
    ria_db = sqlite3.connect('db_archive/ria_db')
    cursor = ria_db.cursor()
    if cursor.execute("""DELETE FROM ria_links"""):
        print('[INFO]: Links deleted from Database')
    else:
        print('WARNING: Something goes wrong')
    ria_db.commit()