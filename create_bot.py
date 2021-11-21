from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token='2110764245:AAFLTkPNITKKdwFyq9Z65EfH0O-EwrWb-s0')
dp = Dispatcher(bot, storage=storage)
