from uuid import UUID

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from pydantic import BaseModel, ValidationError

from core.const import subscriptions

class CatalogFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == 'catalog':
            return {'value': callback.data}
        return False

class BucketFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == 'bucket':
            return {'value': callback.data}
        return False

class SubscriptionFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data in subscriptions:
            return {'value': callback.data}
        return False

class BackFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == 'back':
            return True
        return False

class ForwardFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == 'forward':
            return True
        return False


class UuidValidator(BaseModel):

    id: UUID


class UuidFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        try:
            _ = UuidValidator(id=callback.data)
            return {'value': callback.data}
        except ValidationError:
            return False
