from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery

from core.dependencies import product_service, redis_client
from core.logger import logging
from models.state import FSMmodel
from models.filters import CatalogFilter, BackFilter, ForwardFilter, UuidFilter

router: Router = Router()


@router.callback_query(StateFilter(FSMmodel.catalog,
                                   default_state),
                       UuidFilter())
async def choosen_category(callback: CallbackQuery,
                           value: str,
                           state: FSMContext,
                           service: product_service,
                           red_client: redis_client):
    try:
        subcategories = await service.get_pages_from_cache(value, red_client)
        if not subcategories:
            subcategories = await service.get_subcategories(value)
            await service.put_pages_to_cache(value, subcategories, red_client)
        user_data = await service.get_user_data(state)
        page_number = int(user_data.get('subcategory'))
        if subcategories:
            keybord, page_number = service.prepare_reply(pages=subcategories,
                                                        page_number=page_number,
                                                        context='subcategory')
            await callback.message.edit_text(text='Выберите подкатегорию товара:',
                                            reply_markup=keybord.as_markup())
            await state.update_data(category_uuid=value)
            await state.set_state(FSMmodel.subcategory)
        else:
            await callback.message.edit_text(text='Категория пуста.')

    except Exception as err:
        logging.error(err)
        await callback.message.edit_text(text='Сервис временно не доступен :(...')


@router.callback_query(StateFilter(FSMmodel.subcategory),
                       ForwardFilter())
async def command_forward(callback: CallbackQuery,
                          state: FSMContext,
                          service: product_service,
                          red_client: redis_client):
    try:
        user_data = await service.get_user_data(state)
        value = user_data.get('category_uuid')
        subcategories = await service.get_pages_from_cache(value,
                                                           red_client)
        if not subcategories:
            subcategories = await service.get_subcategories(value)
            await service.put_pages_to_cache(value,
                                             subcategories, red_client)
        page_number = int(user_data.get('subcategory'))
        page_number += 1
        keybord, page_number = service.prepare_reply(pages=subcategories,
                                                     page_number=page_number,
                                                     context='subcategory')
        await state.update_data(subcategory = page_number)
        await callback.message.edit_text(text='Выберите подкатегорию товара:',
                                         reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        await callback.message.edit_text(text='Сервис временно не доступен :(...')


@router.callback_query(StateFilter(FSMmodel.subcategory),
                       BackFilter())
async def command_forward(callback: CallbackQuery,
                          state: FSMContext,
                          service: product_service,
                          red_client: redis_client):
    try:
        user_data = await service.get_user_data(state)
        value = user_data.get('category_uuid')
        subcategories = await service.get_pages_from_cache(value,
                                                           red_client)
        if not subcategories:
            subcategories = await service.get_subcategories(value)
            await service.put_pages_to_cache(value,
                                             subcategories, red_client)
        page_number = int(user_data.get('subcategory'))
        page_number -= 1
        keybord, page_number = service.prepare_reply(pages=subcategories,
                                                     page_number=page_number,
                                                     context='subcategory')
        await state.update_data(subcategory = page_number)
        await callback.message.edit_text(text='Выберите подкатегорию товара:',
                                         reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        await callback.message.edit_text(text='Сервис временно не доступен :(...')
