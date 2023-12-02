from json import dumps, loads

from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from redis.asyncio import Redis
from sqlalchemy import select

from core.const import base_buttons
from core.config import settings
from db.shemas import Category, SubCategory, Item
from models.pagintor import Paginator
from models.item import ItemOut
from services.base_service import BaseService


class ProductService(BaseService, Paginator):

    async def get_categories(self) -> dict:
        stmt = select(Category.name, Category.id).order_by(Category.name)
        result = await self.db.execute(stmt)
        result_items = result.all()
        if result_items:
            categories = [(ele[0], str(ele[1])) for ele in result_items]
            paginated_categories = self.paginate(categories, settings.categories)
            return paginated_categories

    async def get_subcategories(self, id: str) -> dict:
        stmt = select(SubCategory.name,
                      SubCategory.id).where(
                          SubCategory.category_id == id).order_by(
                              SubCategory.name)
        result = await self.db.execute(stmt)
        result_items = result.all()
        if result_items:
            subcategories = [(ele[0], str(ele[1])) for ele in result_items]
            paginated_subcategories = self.paginate(subcategories, settings.categories)
            return paginated_subcategories

    async def get_items(self, id: str) -> dict:
        stmt = select(Item.name, Item.id,
                      Item.description, Item.image_path).where(
                          Item.subcategory_id == id).order_by(
                              Item.name)
        result = await self.db.execute(stmt)
        result_items = result.all()
        if result_items:
            items = [(ele[0], str(ele[1]), ele[2], ele[3]) for ele in result_items]
            paginated_items = self.paginate(items, settings.categories)
            return paginated_items

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

    async def get_choosen_item(self, id: str,
                               state: FSMContext,
                               client: Redis) -> ItemOut:
        try:
            user_data = await self.get_user_data(state)
            page_number = user_data.get('item')
            items_all = await client.get(user_data.get('subcategory_uuid'))
            items_all = loads(items_all)
            items = items_all.get(str(page_number))
            item = next(filter(lambda x: x[1] == id, items))
            item = ItemOut(name=item[0],
                           id=item[1],
                           description=item[2],
                           image_path=item[3])
            return item
        except:
            item = await self.db.get(Item, id)
            item = ItemOut(name=item.name,
                           id=str(item.id),
                           description=item.description,
                           image_path=item.image_path)
            return item

    def prepare_item_show_msg(self, item: ItemOut) -> str:
        res = f'Наименование: {item.name}.\n'
        res += f'Описание: {item.description}.'
        return res

    def prepare_reply(self, pages: dict,
                      context: str = None,
                      page_number: int = 1) -> tuple[InlineKeyboardBuilder, str]:
        builder = InlineKeyboardBuilder()
        total_pages = pages.get('total_pages')
        if page_number > int(total_pages):
            page_number = 1
        if page_number < 1:
            page_number = int(total_pages)
        page_number = str(page_number)
        page = pages.get(page_number)
        for ele in page:
            button_text, callback = ele[0], ele[1]
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
        if context and context == 'item':
            builder.row(*[InlineKeyboardButton(
                text='Вернуться к выбору подкатегории.',
                callback_data='back_to_subcategory')])
        builder.row(*[InlineKeyboardButton(
                text='Перейти в корзину.',
                callback_data='bucket')])
        return builder, page_number