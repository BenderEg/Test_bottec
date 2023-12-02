from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from core.const import show_image_buttons, base_buttons, confirm_buttons, \
    add_quantity_buttons
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
            keybord = service.create_keybord(show_image_buttons)
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
                                             #parse_mode='html',
                                             #disable_web_page_preview=False
                                             )
    except Exception as err:
        logging.error(err)
        keybord = service.create_keybord(base_buttons)
        await state.set_state(state=None)
        await callback.message.edit_text(text='Повторите ввод команды.',
                                         reply_markup=keybord.as_markup())


@router.callback_query(StateFilter(FSMmodel.show_item),
                       AddToBucketFilter())
async def ask_quantity(callback: CallbackQuery,
                       state: FSMContext,
                       service: product_service):
    try:
        keybord = service.create_keybord(add_quantity_buttons)
        await callback.message.edit_text(text='Введите количество товара.',
                                         reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        keybord = service.create_keybord(base_buttons)
        await state.set_state(state=None)
        await callback.message.edit_text(text='Повторите ввод команды.',
                                         reply_markup=keybord.as_markup())

@router.message(StateFilter(FSMmodel.show_item),
                DigitFilter())
async def confirm_quantity(message: Message,
                           state: FSMContext,
                           service: product_service,
                           value: str):
    try:
        user_data = await state.get_data()
        item: dict = user_data.get('current_item')
        item['quantity'] = value
        msg = f"Товар: {item.get('name')}.\n\
Количество: {value}.\n\
Выберите варианты из меню."
        keybord = service.create_keybord(confirm_buttons)
        await state.update_data(current_item=item)
        await message.answer(text=msg, reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        keybord = service.create_keybord(base_buttons)
        await state.set_state(state=None)
        await message.answer(text='Повторите ввод команды.',
                             reply_markup=keybord.as_markup())


@router.callback_query(StateFilter(FSMmodel.show_item),
                       ConfirmationFilter())
async def add_to_bucket(callback: CallbackQuery,
                        state: FSMContext,
                        service: product_service):
    try:
        user_data = await state.get_data()
        item: dict = user_data.get('current_item')
        bucket: dict = user_data.get('bucket')
        bucket[item.get('id')] = item
        keybord = service.create_keybord(base_buttons)
        await state.update_data(bucket=bucket)
        await callback.message.edit_text(text=f"Товар добавлен в корзину.\n\
Выберите дальнейшее действие из списка.",
                                        reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        keybord = service.create_keybord(base_buttons)
        await state.set_state(state=None)
        await callback.message.edit_text(text='Повторите ввод команды.',
                                         reply_markup=keybord.as_markup())