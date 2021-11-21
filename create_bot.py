from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token='2075583508:AAEBpjrIL4Kcj22AMIk61qYsczXXfJ-96z4')
dp = Dispatcher(bot, storage=storage)
