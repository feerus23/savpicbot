from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message
from data.base import Users, Picture
from data.languages import text
from handlers.states import States
from data import bot


async def start(m: Message):
    u = Users(m.from_user.id)
    lang = u.lang()

    if lang is None:
        await m.answer(text['rus']['first_message'])
    else:
        await m.answer(text[lang]['second_message'])
        await States.on_pic_cap.set()


async def on_picture_capture(m: Message):
    uid = m.from_user.id
    lang = Users(uid).lang()

    kw = m.caption if m.caption else "#w"
    print(len(m.photo), m.photo)

    if len(m.photo) > 0:
        Picture(uid, kw, m.photo[-1].file_id)
    else:
        await m.answer(text[lang]['invalid_input'])


def reg(dp: Dispatcher):
    dp.register_message_handler(start)
    dp.register_message_handler(on_picture_capture, state=States.on_pic_cap, content_types=['photo', 'text'])
