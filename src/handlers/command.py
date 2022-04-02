from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, InputMediaPhoto
from aiogram.dispatcher.filters.builtin import CommandStart

from data.base import Users, Picture
from data.languages import text
from . import message

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


async def wki_handler(m: Message, state: FSMContext):
    Picture.edit_default_keyword(m.from_user.id, m.text)
    await m.answer('Done!')
    await state.finish()


def reg(dp: Dispatcher):
    dp.register_message_handler(change_language, commands=cmds['lang'], state="*")
    dp.register_message_handler(settings, commands=cmds['sets'], state="*")
    dp.register_message_handler(message.start, CommandStart(deep_link="picadd"),
                                state="*")
    dp.register_message_handler(wki_handler, state=states.States.wait_kw_input)
