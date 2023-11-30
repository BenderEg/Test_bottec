from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery

from core.dependencies import product_service, redis_client
from core.logger import logging
from models.filters import CatalogFilter

router: Router = Router()

@router.callback_query(StateFilter(default_state),
                       CatalogFilter())
async def subscribe(callback: CallbackQuery,
                    service: product_service,
                    value: str,
                    red_client: redis_client):
    id = callback.from_user.id
    try:
        categories = await service.get_categories()
        await red_client.set(name=value, value=id)

        #await callback.message.edit_text(text='Подписка успешно оформлена!',
         #                                reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        await callback.message.edit_text(text='Сервис временно не доступен :(...')