from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.const import base_buttons, empty_items
from core.dependencies import product_service, redis_client
from core.logger import logging
from models.state import FSMmodel
from models.filters import BackToItemFilter, BackFilter, ForwardFilter, \
    UuidFilter

router: Router = Router()


@router.callback_query(StateFilter(FSMmodel.subcategory),
                       UuidFilter())
async def choosen_subcategory(callback: CallbackQuery,
                           value: str,
                           state: FSMContext,
                           service: product_service,
                           red_client: redis_client):
    try:
        items = await service.get_pages_from_cache(value, red_client)
        if not items:
            items = await service.get_items(value)
            await service.put_pages_to_cache(value, items, red_client)
        user_data = await service.get_user_data(state)
        page_number = int(user_data.get('item'))
        if items:
            keybord, page_number = service.prepare_reply(
                pages=items,
                page_number=page_number,
                context='item')
            await state.update_data(subcategory_uuid=value)
            await callback.message.edit_text(text='Выберите товар из списка:',
                                            reply_markup=keybord.as_markup())
            await state.set_state(FSMmodel.item)
        else:
            keybord = service.create_keybord(empty_items)
            await callback.message.edit_text(text='Перечень товаров пуст.',
                                             reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        keybord = service.create_keybord(base_buttons)
        await state.set_state(state=None)
        await callback.message.edit_text(text='Повторите ввод команды.',
                                         reply_markup=keybord.as_markup())


@router.callback_query(StateFilter(FSMmodel.item),
                       ForwardFilter())
async def command_forward(callback: CallbackQuery,
                          state: FSMContext,
                          service: product_service,
                          red_client: redis_client):
    try:
        user_data = await service.get_user_data(state)
        value = user_data.get('subcategory_uuid')
        items = await service.get_pages_from_cache(value, red_client)
        if not items:
            items = await service.get_items(value)
            await service.put_pages_to_cache(value,
                                             items, red_client)
        page_number = int(user_data.get('item'))
        page_number += 1
        keybord, page_number = service.prepare_reply(pages=items,
                                                     page_number=page_number,
                                                     context='item')
        await state.update_data(item = page_number)
        await callback.message.edit_text(text='Выберите товар из списка:',
                                         reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        keybord = service.create_keybord(base_buttons)
        await state.set_state(state=None)
        await callback.message.edit_text(text='Повторите ввод команды.',
                                         reply_markup=keybord.as_markup())


@router.callback_query(StateFilter(FSMmodel.item),
                       BackFilter())
async def command_back(callback: CallbackQuery,
                       state: FSMContext,
                       service: product_service,
                       red_client: redis_client):
    try:
        user_data = await service.get_user_data(state)
        value = user_data.get('subcategory_uuid')
        items = await service.get_pages_from_cache(value, red_client)
        if not items:
            items = await service.get_items(value)
            await service.put_pages_to_cache(value,
                                             items, red_client)
        page_number = int(user_data.get('item'))
        page_number -= 1
        keybord, page_number = service.prepare_reply(pages=items,
                                                     page_number=page_number,
                                                     context='item')
        await state.update_data(item = page_number)
        await callback.message.edit_text(text='Выберите товар из списка:',
                                         reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        await callback.message.edit_text(text='Сервис временно не доступен :(...')


@router.callback_query(StateFilter(FSMmodel.show_item,
                                   FSMmodel.bucket),
                       BackToItemFilter())
async def back_to_item(callback: CallbackQuery,
                       state: FSMContext,
                       service: product_service,
                       red_client: redis_client):
    user_data = await service.get_user_data(state)
    subcategory = user_data.get('subcategory_uuid')
    await choosen_subcategory(callback, subcategory, state, service, red_client)


# убрать лучше
'''
@router.message(StateFilter(FSMmodel.show_item),
                       Command(commands='cancel'))
async def process_cancel_command(message: CallbackQuery,
                                 state: FSMContext,
                                 service: product_service,
                                 red_client: redis_client):
    try:
        user_data = await service.get_user_data(state)
        subcategory = user_data.get('subcategory_uuid')
        items = await service.get_pages_from_cache(subcategory, red_client)
        if not items:
            items = await service.get_items(subcategory)
            await service.put_pages_to_cache(subcategory, items, red_client)
        user_data = await service.get_user_data(state)
        page_number = int(user_data.get('item'))
        if items:
            keybord, page_number = service.prepare_reply(
                pages=items,
                page_number=page_number,
                context='item')
            await state.update_data(subcategory_uuid=subcategory)
            await message.answer(text='Выберите товар из списка:',
                                 reply_markup=keybord.as_markup())
            await state.set_state(FSMmodel.item)
        else:
            await message.answer(text='Перечень товаров пуст.')
    except Exception as err:
        logging.error(err)
        await message.answer(text='Сервис временно не доступен :(...')
'''