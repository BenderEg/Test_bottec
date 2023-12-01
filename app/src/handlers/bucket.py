from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from core.const import base_buttons
from core.dependencies import bucket_service
from core.logger import logging
from models.filters import BucketFilter
#from core.lexicon import LEXICON_RU
#from models.exeptions import ServerErrorExeption

router: Router = Router()

@router.callback_query(BucketFilter())
async def show_bucket(callback: CallbackQuery,
                      service: bucket_service,
                      state: FSMContext):
    try:
        user_data = await state.get_data()
        bucket: dict = user_data.get('bucket')
        if not bucket:
            keybord = service.create_start_builder(base_buttons)
            await callback.message.edit_text(text='Ваша корзина пуста.\n\
Выберите дальнейшие действия из списка ниже.',
                                             reply_markup=keybord.as_markup())
        else:
            res = service.show_bucket_itmes(bucket)
            await callback.message.answer(text='Вы в корзинке.')
    except Exception as err:
        logging.error(err)
        await callback.message.answer(text='Сервис временно не доступен :(...')