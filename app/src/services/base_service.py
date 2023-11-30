from aiogram.fsm.context import FSMContext
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
            'bucket': {}
        }
        await state.set_data(data)
        return data