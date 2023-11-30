from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery

from core.const import base_buttons
from core.dependencies import user_service
from core.logger import logging
from models.filters import SubscriptionFilter

router: Router = Router()

@router.callback_query(StateFilter(default_state),
                       SubscriptionFilter())
async def subscribe(callback: CallbackQuery,
                    service: user_service,
                    value: str):
    id = callback.from_user.id
    try:
        if value == 'group_subscription':
            await service.add_group_subscription(id)
        elif value == 'channel_subscription':
            await service.add_channel_subscription(id)
        else:
            await service.add_all_subscription(id)
        keybord = service.create_start_builder(base_buttons)
        await callback.message.edit_text(text='Подписка успешно оформлена!',
                                         reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        await callback.message.edit_text(text='Сервис временно не доступен :(...')