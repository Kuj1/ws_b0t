import sqlite3


def sql_connect():
    # global olx_db, cursor
    olx_db = sqlite3.connect('olx_db')
    cursor = olx_db.cursor()
    if olx_db:
        print('[INFO]: Database is connected')
    olx_db.execute("""CREATE TABLE IF NOT EXISTS olx_links(link TEXT)""")
    olx_db.commit()


async def sql_add_link(state):
    olx_db = sqlite3.connect('olx_db')
    cursor = olx_db.cursor()
    async with state.proxy() as url:
        cursor.execute("""INSERT INTO olx_links VALUES(?)""", tuple(url.values()))
        olx_db.commit()

