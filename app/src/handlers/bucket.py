from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, FSInputFile

from core.const import base_buttons
from core.dependencies import user_service
from core.logger import logging
from models.filters import BucketFilter
#from core.lexicon import LEXICON_RU
#from models.exeptions import ServerErrorExeption

router: Router = Router()

@router.callback_query(BucketFilter())
async def show_bucket(callback: CallbackQuery,
                      service: user_service,
                      state: FSMContext,
                      value: str):
    try:
        user_data = await state.get_data()
        bucket = user_data.get('bucket')
        if not bucket:
            keybord = service.create_start_builder(base_buttons)
            #image = FSInputFile(path='media/Test_image.png')
            #await callback.message.answer_photo(image)
            await callback.message.answer(text='Ваша корзина пуста.',
                                          reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        await callback.message.answer(text='Сервис временно не доступен :(...')