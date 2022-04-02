from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import InlineQuery, InlineQueryResultCachedPhoto
from data.base import Users, Picture
from data.languages import text


def get_result(p: Picture, start_num):
    res = p()
    overall_items = len(res)

    if start_num >= overall_items:
        return []
    elif start_num + 50 >= overall_items:
        return res[start_num-1:overall_items]
    else:
        return res[start_num-1:start_num + 50]


async def request(q: InlineQuery):
    query_offset = int(q.offset) if q.offset else 1

    t = q.query
    try:
        if t[0] == '#':
            t = t.replace('#', '', 1)
    except IndexError:
        pass

    uid = q.from_user.id
    lang = Users(uid).lang()
    res = get_result(Picture(uid, keyword=t), query_offset)

    photos = [InlineQueryResultCachedPhoto(id=item[0][:50], photo_file_id=item[0]) for item in res]

    if len(photos) < 50:
        await q.answer(photos,
                       cache_time=60,
                       is_personal=True,
                       switch_pm_text=text[lang]["add_pic"],
                       switch_pm_parameter="picadd",
                       next_offset=''
                       )
    else:
        await q.answer(photos,
                       cache_time=60,
                       is_personal=True,
                       switch_pm_text=text[lang]["add_pic"],
                       switch_pm_parameter="picadd",
                       next_offset=str(query_offset + 15)
                       )


def reg(dp: Dispatcher):
    dp.register_inline_handler(request, state="*")
