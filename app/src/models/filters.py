from uuid import UUID

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from pydantic import BaseModel, ValidationError

from core.const import subscriptions
from models.item import Digit

class CatalogFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == 'catalog':
            return {'value': callback.data}
        return False

class BackToCategoryFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == 'back_to_subcategory':
            return True
        return False

class BackToItemFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == 'back_to_item':
            return True
        return False

class BucketFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == 'bucket':
            return True
        return False

class AddToBucketFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == 'add_to_bucket':
            return True
        return False

class BucketDeleteFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data in ('delete_item', 'clear_bucket'):
            return {'value': callback.data}
        return False

class OrderFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == 'order':
            return True
        return False

class CheckAdressFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == 'change_adress':
            return True
        return False

class PaymentFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == 'payment':
            return True
        return False

class ConfirmationFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == 'yes':
            return True
        return False

class DigitFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            _ = Digit(value=message.text)
            return {'value': message.text}
        except ValidationError:
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

class TextFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text:
            return {'value': message.text}
        return False