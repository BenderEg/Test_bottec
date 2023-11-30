from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select

from core.const import base_buttons
from core.config import settings
from db.shemas import User, Category
from models.pagintor import Paginator
from services.base_service import BaseService


class ProductService(BaseService, Paginator):

    async def get_categories(self) -> User:
        stmt = select(Category.id, Category.name)
        result = await self.db.execute(stmt)
        categories = [(str(ele[0]), ele[1]) for ele in result.all()]
        paginated_categories = self.paginate(categories, settings.categories)
        print(paginated_categories)
        return paginated_categories
