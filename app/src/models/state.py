from aiogram.filters.state import State, StatesGroup


class FSMmodel(StatesGroup):
    catalog = State()
    subcategory = State()
    item = State()
    bucket = State()
    show_item = State()