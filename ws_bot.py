import logging
from aiogram.utils import executor
from create_bot import dp
from handlers import client, common
from db import olx_db, ria_db
# from config.config_reader import load_config

logging.basicConfig(level=logging.INFO)


async def startup(_):
    olx_db.sql_connect_olx()
    ria_db.sql_connect_to_ria()


client.register_client_handlers(dp)
common.register_common_handlers(dp)


def main():
    executor.start_polling(dp, skip_updates=True, on_startup=startup)


if __name__ == '__main__':
    main()


