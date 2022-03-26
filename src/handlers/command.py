from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, InputMediaPhoto

from data.base import Users, Picture
from data.languages import text
from data import bot

from keyboards import pic_edit_keyboard as pe_kb
from . import states

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
    u = Users(m.from_user.id)
    l = u.lang()
    await m.answer(text[l]['set_keyword'])
    await states.States.wait_kw_input.set()


async def show_my_saves(m: Message):
    u = Users(m.from_user.id)
    l = u.lang()
    await m.answer(text[l]['send_keyword'])


async def next(m: Message):
    pics = Picture(m.from_user.id)()
    u = Users(m.from_user.id)
    lst = u.storage('saved_pics', default=[])

    if not (len(lst)):
        for i, v in enumerate(pics):
            if i % 10:
                lst[i // 10] += [v]
            else:
                lst.append([v])

        u.storage(saved_pics=lst)

    media = [InputMediaPhoto(pic, caption="#" + str(i)) for i, pic in enumerate(lst[0])]

    await m.answer_media_group(media, )


async def wki_handler(m: Message, state: FSMContext):
    Picture.edit_default_keyword(m.from_user.id, m.text)
    await m.answer('Done!')
    await state.finish()


def reg(dp: Dispatcher):
    dp.register_message_handler(change_language, commands=cmds['lang'], state="*")
    dp.register_message_handler(settings, commands=cmds['sets'], state="*")
    dp.register_message_handler(wki_handler, state=states.States.wait_kw_input)
