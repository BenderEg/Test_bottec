from json import dumps, loads
from typing import List
from uuid import UUID

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from redis.asyncio import Redis
from sqlalchemy import select

from core.const import base_buttons
from core.config import settings
from db.shemas import Category, SubCategory
from models.pagintor import Paginator
from services.base_service import BaseService


class ProductService(BaseService, Paginator):

    async def get_categories(self) -> dict:
        stmt = select(Category.name, Category.id).order_by(Category.name)
        result = await self.db.execute(stmt)
        categories = [(ele[0], str(ele[1])) for ele in result.all()]
        paginated_categories = self.paginate(categories, settings.categories)
        return paginated_categories

    async def get_subcategories(self, id: UUID) -> dict:
        stmt = select(SubCategory.name,
                      SubCategory.id).where(
                          SubCategory.category_id == id).order_by(
                              SubCategory.name)
        result = await self.db.execute(stmt)
        subcategories = [(ele[0], str(ele[1])) for ele in result.all()]
        paginated_subcategories = self.paginate(subcategories, settings.categories)
        return paginated_subcategories

    async def put_pages_to_cache(self, name: str,
                                 pages: dict,
                                 client: Redis) -> None:
        await client.set(name=name, value=dumps(pages),
                         ex=settings.cache_exp)

    async def get_pages_from_cache(self, name: str,
                                    client: Redis) -> dict:
        pages = await client.get(name=name)
        if pages:
            return loads(pages)

    def prepare_reply(self, pages: dict,
                      context: str = None,
                      page_number: int = 1) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()
        total_pages = pages.get('total_pages')
        if page_number > int(total_pages):
            page_number = 1
        if page_number < 1:
            page_number = int(total_pages)
        page_number = str(page_number)
        page = pages.get(page_number)
        for ele in page:
            button_text, callback = ele
            builder.button(text=button_text,
                           callback_data=callback)
        builder.adjust(1)
        if int(total_pages) > 1:
            position = f"{page_number}/{total_pages}"
            navigation_buttons = [InlineKeyboardButton(text='<<', callback_data='back'),
                                InlineKeyboardButton(text=position, callback_data='None'),
                                InlineKeyboardButton(text='>>', callback_data='forward')]
            builder.row(*navigation_buttons)
        if context and context == 'subcategory':
            builder.row(*[InlineKeyboardButton(
                text='Вернуться к выбору категории.',
                callback_data='catalog')])
        builder.row(*[InlineKeyboardButton(
                text='Перейти в корзину.',
                callback_data='bucket')])
        return builder, page_number