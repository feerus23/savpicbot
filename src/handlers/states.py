from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    """
    on_pic_cap0: Первый state для сохранения картиночек (в случае если пользователь пришлёт либо картинку вместе с
    ключом, либо сначала ключ, потом картинку)
    on_pic_cap1: State сохранения картинки когда ключ отправляется отдельным сообщением перед отправкой самой
    картинки.
    wait_kw_input: State из /settings для смены ключа по дефолту
    """
    on_pic_cap0 = State()
    on_pic_cap1 = State()
    wait_kw_input = State()
