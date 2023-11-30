from aiogram.filters.state import State, StatesGroup


class FSMmodel(StatesGroup):
    training = State()
    add = State()
    delete = State()
    add_category = State()
    choose_category = State()