from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message
from data.base import Users
from . import message

cmds = {
    "lang": ['eng', 'rus'],
    "sets": ['settings', 'sets']
}


async def change_language(m: Message):
    t = m.text.replace('/', '')
    await m.answer('Done!')
    Users(m.from_user.id).lang(t)
    return


async def settings(m: Message):
    await m.answer('Work in progress!')


def reg(dp: Dispatcher):
    dp.register_message_handler(change_language, commands=cmds['lang'], state="*")
    dp.register_message_handler(settings, commands=cmds['sets'], state="*")
