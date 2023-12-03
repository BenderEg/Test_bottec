from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.const import base_buttons, bucket_buttons, empty_bucket, \
    payment_gates, payment_gates_change_adress, all_items_deleted_from_bucket
from core.dependencies import bucket_service
from core.logger import logging
from models.filters import BucketFilter, BucketDeleteFilter, OrderFilter, \
    TextFilter, CheckAdressFilter, PaymentFilter, UuidFilter
from models.state import FSMmodel

router: Router = Router()

@router.callback_query(BucketFilter())
async def show_bucket(callback: CallbackQuery,
                      service: bucket_service,
                      state: FSMContext):
    try:
        user_data = await state.get_data()
        bucket: dict = user_data.get('bucket')
        if not bucket:
            keybord = service.create_keybord(empty_bucket)
            await callback.message.edit_text(text='Ваша корзина пуста.\n\
Выберите дальнейшие действия из списка ниже.',
                                             reply_markup=keybord.as_markup())
        else:
            res = service.show_bucket_itmes(bucket)
            keybord = service.create_keybord(bucket_buttons)
            await callback.message.edit_text(text=res,
                                             reply_markup=keybord.as_markup())
            await state.set_state(FSMmodel.bucket)
    except Exception as err:
        logging.error(err)
        keybord = service.create_keybord(base_buttons)
        await state.set_state(state=None)
        await callback.message.edit_text(text='Повторите ввод команды.',
                                         reply_markup=keybord.as_markup())


@router.callback_query(StateFilter(FSMmodel.bucket),
                       BucketDeleteFilter())
async def delete_from_bucket(callback: CallbackQuery,
                             service: bucket_service,
                             value: str,
                             state: FSMContext):
    try:
        user_data = await state.get_data()
        bucket: dict = user_data.get('bucket')
        if value == 'delete_item':
            keybord = service.show_for_delete_items(bucket)
            await callback.message.edit_text(text='Выберите товар для удаления из корзины.',
                                                reply_markup=keybord.as_markup())
        else:
            await state.update_data(bucket={})
            keybord = service.create_keybord(base_buttons)
            await callback.message.edit_text(text='Корзина очищена.',
                                             reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        keybord = service.create_keybord(base_buttons)
        await state.set_state(state=None)
        await callback.message.edit_text(text='Повторите ввод команды.',
                                         reply_markup=keybord.as_markup())


@router.callback_query(StateFilter(FSMmodel.bucket),
                       UuidFilter())
async def delete_item(callback: CallbackQuery,
                      service: bucket_service,
                      value: str,
                      state: FSMContext):
    try:
        user_data = await state.get_data()
        bucket: dict = user_data.get('bucket')
        bucket.pop(value)
        await state.update_data(bucket=bucket)
        if bucket:
            keybord = service.show_for_delete_items(bucket)
            await callback.message.edit_text(text='Выберите товар для удаления из корзины.',
                                             reply_markup=keybord.as_markup())
        else:
            keybord = service.create_keybord(all_items_deleted_from_bucket)
            await callback.message.edit_text(text='Корзина пуста. Выберите дальнейшие действия.',
                                             reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        keybord = service.create_keybord(base_buttons)
        await state.set_state(state=None)
        await callback.message.edit_text(text='Повторите ввод команды.',
                                         reply_markup=keybord.as_markup())


@router.callback_query(StateFilter(FSMmodel.bucket),
                       OrderFilter())
async def check_adress(callback: CallbackQuery,
                       service: bucket_service,
                       state: FSMContext):
    try:
        user_data = await state.get_data()
        adress: str = user_data.get('adress')
        if not adress:
            keybord = service.create_keybord(base_buttons)
            await callback.message.edit_text(text='Введите адресс доставки.',
                                            reply_markup=keybord.as_markup())
        if adress:
            msg = f"Указанный ранее адрес: '{adress}'.\n\
Выберите дальнейшие действия из списка ниже."
            keybord = service.create_keybord(payment_gates_change_adress)
            await callback.message.edit_text(text='Выберите дальнейшие действия из списка ниже.',
                                            reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        keybord = service.create_keybord(base_buttons)
        await state.set_state(state=None)
        await callback.message.edit_text(text='Повторите ввод команды.',
                                         reply_markup=keybord.as_markup())


@router.callback_query(StateFilter(FSMmodel.bucket),
                       CheckAdressFilter())
async def change_adress(callback: CallbackQuery,
                        service: bucket_service,
                        state: FSMContext):
    try:
        keybord = service.create_keybord(base_buttons)
        await callback.message.edit_text(text='Введите адресс доставки.',
                                        reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        keybord = service.create_keybord(base_buttons)
        await state.set_state(state=None)
        await callback.message.edit_text(text='Повторите ввод команды.',
                                         reply_markup=keybord.as_markup())


@router.message(StateFilter(FSMmodel.bucket),
                TextFilter())
async def add_addres(message: Message,
                     value: str,
                     service: bucket_service,
                     state: FSMContext):
    try:
        await state.update_data(adress=value)
        keybord = service.create_keybord(payment_gates)
        msg = f"Адрес: '{value}' принят.\n\
    Выберите дальнейшие действия из списка ниже."
        await message.answer(text=msg,
                            reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        keybord = service.create_keybord(base_buttons)
        await state.set_state(state=None)
        await message.answer(text='Повторите ввод команды.',
                             reply_markup=keybord.as_markup())


@router.callback_query(StateFilter(FSMmodel.bucket),
                       PaymentFilter())
async def make_order(callback: CallbackQuery,
                     service: bucket_service,
                     state: FSMContext):
    try:
        id = callback.from_user.id
        user_data = await state.get_data()
        adress: str = user_data.get('adress')
        bucket: dict = user_data.get('bucket')
        await service.create_order(id, adress, bucket)
        await state.update_data(bucket={})
        keybord = service.create_keybord    (base_buttons)
        await callback.message.edit_text(text='Заказ оформлен. Спасибо!',
                                        reply_markup=keybord.as_markup())
    except Exception as err:
        logging.error(err)
        keybord = service.create_keybord(base_buttons)
        await state.set_state(state=None)
        await callback.message.edit_text(text='Повторите ввод команды.',
                                         reply_markup=keybord.as_markup())