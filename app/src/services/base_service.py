from typing import List

from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from db.shemas import User

class BaseService():

    def __init__(self, db: AsyncSession) -> None:

        self.db = db

    async def get_user_by_id(self, id: int) -> User:
        user = await self.db.get(User, id)
        return user

    async def get_user_data(self, state: FSMContext) -> dict:
        data = await state.get_data()
        if data:
            return data
        data = {
            'catalog': '1',
            'subcategory': '1',
            'item': '1',
            'category_uuid': None,
            'subcategory_uuid': None,
            'current_item': None,
            'bucket': {},
            'adress': None
        }
        await state.set_data(data)
        return data

    def create_start_builder(self, objects: List[tuple] | tuple) \
        -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()
        for ele in objects:
            button_text, callback = ele
            builder.button(text=button_text,
                           callback_data=callback)
        builder.adjust(1)
        return builder