from aiogram.dispatcher import Dispatcher
from os import getenv as ENV
from aiogram.bot import Bot


token = ENV("TOKEN")

bot = Bot(token)
dispatcher = Dispatcher(bot)
