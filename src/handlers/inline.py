from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, InlineQuery, InlineQueryResultCachedPhoto
from data.base import Users, Picture
from data.languages import text
from data import bot


async def request(q: InlineQuery):
    t = q.query
    uid = q.from_user.id
    lang = Users(uid).lang()
    res = Picture(uid, keyword=t).get()

    if len(res) == 0:
        if '#' in t:
            t.replace('#', '')
        else:
            t = '#' + t
        res = Picture(uid, keyword=t).get()

    photos = [InlineQueryResultCachedPhoto(id=item[0][:64], photo_file_id=item[0]) for item in res]

    await q.answer(photos, cache_time=60, is_personal=True)


def reg(dp: Dispatcher):
    dp.register_inline_handler(request)