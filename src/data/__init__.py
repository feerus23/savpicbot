from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from os import getenv
from aiogram.bot import Bot


token = getenv("TOKEN")

bot = Bot(token)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
