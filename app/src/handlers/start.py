from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from core.dependencies import user_service
from core.logger import logging
#from core.lexicon import LEXICON_RU
#from models.exeptions import ServerErrorExeption

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
        await message.answer(text='Сервис временно не доступен :(...')