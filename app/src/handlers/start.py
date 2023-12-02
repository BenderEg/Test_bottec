from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.const import base_buttons
from core.dependencies import user_service
from core.logger import logging

router: Router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message,
                                service: user_service,
                                state: FSMContext):
    id = message.from_user.id
    name = message.from_user.first_name
    try:
        msg, keybord = await service.start(id, name)
        await message.answer(text=msg,
                             reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        keybord = service.create_keybord(base_buttons)
        await state.set_state(state=None)
        await message.answer(text='Повторите ввод команды.',
                             reply_markup=keybord.as_markup())