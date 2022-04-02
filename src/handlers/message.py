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
        await m.answer(text[lang]['second_message']('#' + str(u(0))[2:-3]))
        await States.on_pic_cap0.set()


async def on_picture_capture(m: Message, state: FSMContext):
    uid = m.from_user.id
    u = Users(uid)
    lang = u.lang()

    kw = m.caption if m.caption else "w"

    if len(m.photo) > 0:
        Picture(uid, kw.replace('#', '', 1) if kw[0] == '#' else kw, m.photo[-1].file_id)
    else:
        await m.answer(text[lang]['send_photo'])
        await state.update_data(keyword=m.text.replace('#', '', 1) if m.text[0] == '#' else m.text)
        await States.on_pic_cap1.set()


async def on_picture_capture_1(m: Message, state: FSMContext):
    uid = m.from_user.id
    u = Users(uid)
    lang = u.lang()
    an = await state.get_data()

    if len(m.photo) > 0:
        Picture(uid, an['keyword'], m.photo[-1].file_id)
    else:
        await m.answer(text[lang]["invalid_input"])


def reg(dp: Dispatcher):
    dp.register_message_handler(start)
    dp.register_message_handler(on_picture_capture, state=States.on_pic_cap0, content_types=['photo', 'text'])
    dp.register_message_handler(on_picture_capture_1, state=States.on_pic_cap1, content_types=['photo', 'text'])
