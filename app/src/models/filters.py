from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from pydantic import BaseModel, ValidationError

from core.const import start_callback, subscriptions

class CatalogFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == 'catalog':
            return {'value': callback.data}
        return False


class SubscriptionFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data in subscriptions:
            return {'value': callback.data}
        return False