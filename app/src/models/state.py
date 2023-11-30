from aiogram.filters.state import State, StatesGroup


class FSMmodel(StatesGroup):
    catalog = State()
    subcategory = State()
    delete = State()
    add_category = State()
    choose_category = State()