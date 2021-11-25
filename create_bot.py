from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config.config_reader import load_config

config = load_config("config/ws_bot.ini")

storage = MemoryStorage()
bot = Bot(token=config.ws_bot.token)
dp = Dispatcher(bot, storage=storage)
