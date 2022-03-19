from aiogram.dispatcher import Dispatcher
from aiogram.types import Message
from data.base import Users
from data.languages import text


async def start(m: Message):
    u = Users(m.from_user.id)
    lang = u.lang()

    if u():
        await m.answer(text[lang]['already_specified'])
    else:
        await m.answer(text[lang]['first_message'])


def reg(dp: Dispatcher):
    dp.register_message_handler(start)
