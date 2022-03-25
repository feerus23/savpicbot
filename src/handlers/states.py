from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    on_pic_cap0 = State()
    on_pic_cap1 = State()
    wait_kw_input = State()
