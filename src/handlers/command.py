from aiogram.dispatcher import Dispatcher
from aiogram.types import Message
from data.base import Users

cmds = {
    "lang": ['eng', 'rus']
}


async def change_language(m: Message):
    t = m.text.replace('/', '')

    if t in cmds['lang']:
        Users(m.from_user.id).lang(t)
    else:
        await m.answer('Unavailable language.')


def reg(dp: Dispatcher):
    dp.register_message_handler(change_language, commands=cmds['lang'])
