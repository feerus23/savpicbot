from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.types import BotCommand
from aiogram.bot import Bot
from handlers.command import cmds
from os import getenv

c = cmds
token = getenv("TOKEN")

bot = Bot(token)
dispatcher = Dispatcher(bot, storage=MemoryStorage())


async def register_commands(dp: Dispatcher):
    cmdss = [
                BotCommand(c['sets'][0], "User settings")
            ] + [
                BotCommand(cmd, "change language") for cmd in c['lang']
            ]

    await dp.bot.set_my_commands(cmdss)
