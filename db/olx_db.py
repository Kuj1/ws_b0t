import sqlite3
import os


def sql_connect_olx():
    if os.path.exists('db_archive/'):
        pass
    else:
        os.mkdir('db_archive/')
    olx_db = sqlite3.connect('db_archive/olx_db')
    cursor = olx_db.cursor()
    if olx_db:
        print('[INFO]: Database is connected')
    olx_db.execute("""CREATE TABLE IF NOT EXISTS olx_links (link TEXT, CONSTRAINT uc UNIQUE (link))""")
    olx_db.commit()


async def sql_add_link(state):
    olx_db = sqlite3.connect('db_archive/olx_db')
    cursor = olx_db.cursor()

    async with state.proxy() as url:
        cursor.execute("""INSERT OR IGNORE INTO olx_links VALUES(?)""", tuple(url.values()))
        olx_db.commit()


async def sql_read_olx_link():
    olx_db = sqlite3.connect('db_archive/olx_db')
    cursor = olx_db.cursor()
    return cursor.execute("""SELECT * FROM olx_links""").fetchall()


async def sql_remove_olx_link():
    olx_db = sqlite3.connect('db_archive/olx_db')
    cursor = olx_db.cursor()
    if cursor.execute("""DELETE FROM olx_links"""):
        print('[INFO]: Links deleted from Database')
    else:
        print('WARNING: Something goes wrong')
    olx_db.commit()