from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.const import base_buttons
from core.dependencies import product_service, redis_client
from core.logger import logging
from models.state import FSMmodel
from models.filters import CatalogFilter, BackFilter, ForwardFilter

router: Router = Router()

@router.callback_query(CatalogFilter())
async def show_catalog(callback: CallbackQuery,
                       state: FSMContext,
                       service: product_service,
                       value: str,
                       red_client: redis_client):
    try:
        categories = await service.get_pages_from_cache(value, red_client)
        if not categories:
            categories = await service.get_categories()
            await service.put_pages_to_cache(value, categories, red_client)
        user_data = await service.get_user_data(state)
        page_number = int(user_data.get('catalog'))
        if categories:
            keybord, page_number = service.prepare_reply(pages=categories,
                                                        page_number=page_number)
            await callback.message.edit_text(text='Выберите категорию товаров:',
                                            reply_markup=keybord.as_markup())
            await state.set_state(FSMmodel.catalog)
        else:
            keybord = service.create_keybord(base_buttons)
            await callback.message.edit_text(text='Нет доступных категорий.',
                                             reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        keybord = service.create_keybord(base_buttons)
        await state.set_state(state=None)
        await callback.message.edit_text(text='Повторите ввод команды.',
                                         reply_markup=keybord.as_markup())


@router.callback_query(StateFilter(FSMmodel.catalog),
                       ForwardFilter())
async def command_forward(callback: CallbackQuery,
                          state: FSMContext,
                          service: product_service,
                          red_client: redis_client):
    try:
        categories = await service.get_pages_from_cache('catalog', red_client)
        if not categories:
            categories = await service.get_categories()
            await service.put_pages_to_cache('catalog', categories, red_client)
        user_data = await service.get_user_data(state)
        page_number = int(user_data.get('catalog'))
        page_number += 1
        keybord, page_number = service.prepare_reply(pages=categories,
                                                     page_number=page_number)
        await state.update_data(catalog = page_number)
        await callback.message.edit_text(text='Выберите категорию товаров:',
                                         reply_markup=keybord.as_markup())
        await state.set_state(FSMmodel.catalog)
    except Exception as err:
        logging.error(err)
        keybord = service.create_keybord(base_buttons)
        await state.set_state(state=None)
        await callback.message.edit_text(text='Повторите ввод команды.',
                                         reply_markup=keybord.as_markup())


@router.callback_query(StateFilter(FSMmodel.catalog),
                       BackFilter())
async def command_back(callback: CallbackQuery,
                          state: FSMContext,
                          service: product_service,
                          red_client: redis_client):
    try:
        categories = await service.get_pages_from_cache('catalog', red_client)
        if not categories:
            categories = await service.get_categories()
            await service.put_pages_to_cache('catalog', categories, red_client)
        user_data = await service.get_user_data(state)
        page_number = int(user_data.get('catalog'))
        page_number -= 1
        keybord, page_number = service.prepare_reply(pages=categories,
                                                     page_number=page_number)
        await state.update_data(catalog = page_number)
        await callback.message.edit_text(text='Выберите категорию товаров:',
                                         reply_markup=keybord.as_markup())
        await state.set_state(FSMmodel.catalog)
    except Exception as err:
        logging.error(err)
        keybord = service.create_keybord(base_buttons)
        await state.set_state(state=None)
        await callback.message.edit_text(text='Повторите ввод команды.',
                                         reply_markup=keybord.as_markup())
