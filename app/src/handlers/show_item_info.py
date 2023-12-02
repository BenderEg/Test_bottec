from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, FSInputFile, Message

from core.const import show_image_buttons, base_buttons, confirm_buttons
from core.config import settings
from core.dependencies import product_service, redis_client
from core.logger import logging
from models.state import FSMmodel
from models.filters import UuidFilter, AddToBucketFilter, DigitFilter, \
    ConfirmationFilter

router: Router = Router()

@router.callback_query(StateFilter(FSMmodel.item),
                       UuidFilter())
async def choosen_item(callback: CallbackQuery,
                       value: str,
                       state: FSMContext,
                       service: product_service,
                       red_client: redis_client):
    try:
        item = await service.get_choosen_item(value, state, red_client)
        if item:
            msg = service.prepare_item_show_msg(item)
            keybord = service.create_start_builder(show_image_buttons)
            await state.set_state(FSMmodel.show_item)
            await state.update_data(current_item=item.model_dump())
            url = f'{settings.server_link}/media/{item.image_path}'
            msg += f'<a href="{url}">&#8205;</a>'
            # альтернатива с отправкой photo+caption
            # msg = service.prepare_item_show_msg(item)
            # image = FSInputFile(path=f'media/{item.image_path}')
            #await callback.message.answer_photo(photo=image, caption=msg)
            await callback.message.edit_text(text=msg,
                                             reply_markup=keybord.as_markup(),
                                             parse_mode='html',
                                             disable_web_page_preview=False
                                             )
    except Exception as err:
        logging.error(err)
        await callback.message.edit_text(text='Сервис временно не доступен :(...')


@router.callback_query(StateFilter(FSMmodel.show_item),
                       AddToBucketFilter())
async def ask_quantity(callback: CallbackQuery):
    await callback.message.answer(text='Введите количество товара.\n\
Для возврата к перечню товаров нажмите /cancel.')


@router.message(StateFilter(FSMmodel.show_item),
                DigitFilter())
async def confirm_quatity(message: Message,
                          state: FSMContext,
                          service: product_service,
                          value: str):

    user_data = await state.get_data()
    item: dict = user_data.get('current_item')
    item['quantity'] = value
    msg = f"Товар: {item.get('name')}.\n\
Количество: {value}.\n\
Выберите варианты из меню."
    keybord = service.create_start_builder(confirm_buttons)
    await state.update_data(current_item=item)
    await message.answer(text=msg, reply_markup=keybord.as_markup())


@router.callback_query(StateFilter(FSMmodel.show_item),
                       ConfirmationFilter())
async def add_to_bucket(callback: CallbackQuery,
                        state: FSMContext,
                        service: product_service):
    user_data = await state.get_data()
    item: dict = user_data.get('current_item')
    bucket: dict = user_data.get('bucket')
    bucket[item.get('id')] = item
    keybord = service.create_start_builder(base_buttons)
    await state.update_data(bucket=bucket)
    await callback.message.edit_text(text=f"Товар добавлен в корзину.\n\
Выберите дальнейшее действие из списка.",
                                     reply_markup=keybord.as_markup())