from datetime import datetime, timedelta

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from handlers.states import CreateTaskStates
from keyboards.kb_cancel_time import (make_kb_change_unit, month_list, make_kb_month, make_kb_year, make_kb_days,
                                      make_kb_hour, make_kb_minute)
from static.font_styles import B_TEXT
from filters import CheckIntText, correct_day
from storage.manage_storage import add_task

router = Router()


@router.callback_query(CreateTaskStates.create_cancel_time, F.data == 'default_time')
async def default_time(query: types.CallbackQuery, state: FSMContext) -> None:
    cancel_time = datetime.now() + timedelta(days=1)
    data: dict = await state.get_data()
    add_task(user_id=query.from_user.id, title=data['title'], description=data['description'], cancel_task=cancel_time)
    await query.message.edit_text('Задача поставлена!')
    await state.clear()
    await query.answer()


@router.callback_query(CreateTaskStates.create_cancel_time, F.data == 'change_datetime')
async def create_cancel_time(query: types.CallbackQuery, state: FSMContext) -> None:
    keyboard: types.InlineKeyboardMarkup = await make_kb_change_unit()
    await state.set_state(CreateTaskStates.cancel_time_day)
    this_day = str(datetime.now().day)
    await query.message.edit_text(text=f'Выбрать текущий день: {B_TEXT.format(this_day)}',
                                  reply_markup=keyboard,
                                  parse_mode='HTML')


@router.callback_query(CreateTaskStates.cancel_time_day, F.data == 'this')
@router.callback_query(CreateTaskStates.cancel_time_day, F.data, CheckIntText())
async def cancel_time_day(query: types.CallbackQuery, state: FSMContext, number: int | None = None) -> None:
    this_datetime = datetime.now()
    this_month: str = month_list[this_datetime.month - 1]
    keyboard: types.InlineKeyboardMarkup = await make_kb_change_unit()
    day: int = number or this_datetime.day
    await state.update_data(day=day)
    await state.set_state(CreateTaskStates.cancel_time_month)
    await query.message.edit_text(text=f'Выбрать текущий месяц: {B_TEXT.format(this_month)}',
                                  reply_markup=keyboard,
                                  parse_mode='HTML')


@router.callback_query(CreateTaskStates.cancel_time_day, F.data == 'change')
async def cancel_time_day_change(query: types.CallbackQuery) -> None:
    keyboard: types.InlineKeyboardMarkup = await make_kb_days()
    await query.message.edit_text(text='Выберите день', reply_markup=keyboard)


@router.callback_query(CreateTaskStates.cancel_time_month, F.data == 'this')
@router.callback_query(CreateTaskStates.cancel_time_month, F.data, CheckIntText())
async def cancel_time_month(query: types.CallbackQuery, state: FSMContext, number: int | None = None) -> None:
    keyboard: types.InlineKeyboardMarkup = await make_kb_change_unit()
    this_datetime = datetime.now()
    month: int = number or this_datetime.month
    await state.update_data(month=month)
    await state.set_state(CreateTaskStates.cancel_time_year)
    await query.message.edit_text(text=f'Выбрать текущий год: {B_TEXT.format(this_datetime.year)}',
                                  reply_markup=keyboard,
                                  parse_mode='HTML')


@router.callback_query(CreateTaskStates.cancel_time_month, F.data == 'change')
async def cancel_time_month_change(query: types.CallbackQuery) -> None:
    keyboard: types.InlineKeyboardMarkup = await make_kb_month()
    await query.message.edit_text(text='Выберите месяц', reply_markup=keyboard)


@router.callback_query(CreateTaskStates.cancel_time_year, F.data == 'this')
@router.callback_query(CreateTaskStates.cancel_time_year, F.data, CheckIntText())
async def cancel_time_year(query: types.CallbackQuery, state: FSMContext, number: int | None = None) -> None:
    keyboard: types.InlineKeyboardMarkup = await make_kb_change_unit()
    this_datetime = datetime.now()
    year: int = number or datetime.month
    await state.update_data(year=year)
    await state.set_state(CreateTaskStates.cancel_time_hour)
    await query.message.edit_text(text=f'Выбрать текущий час: {B_TEXT.format(this_datetime.hour)}',
                                  reply_markup=keyboard,
                                  parse_mode='HTML')


@router.callback_query(CreateTaskStates.cancel_time_year, F.data == 'change')
async def cancel_time_year_change(query: types.CallbackQuery) -> None:
    keyboard: types.InlineKeyboardMarkup = await make_kb_year()
    await query.message.edit_text(text='Выберите год', reply_markup=keyboard)


@router.callback_query(CreateTaskStates.cancel_time_hour, F.data == 'this')
@router.callback_query(CreateTaskStates.cancel_time_hour, F.data, CheckIntText())
async def cancel_time_hour(query: types.CallbackQuery, state: FSMContext, number: int | None = None) -> None:
    keyboard: types.InlineKeyboardMarkup = await make_kb_change_unit()
    this_datetime = datetime.now()
    hour: int = number or this_datetime.hour
    await state.update_data(hour=hour)
    await state.set_state(CreateTaskStates.cancel_time_minute)
    await query.message.edit_text(text=f'Выбрать текущую минуту: {B_TEXT.format(this_datetime.minute)}',
                                  reply_markup=keyboard,
                                  parse_mode='HTML')


@router.callback_query(CreateTaskStates.cancel_time_hour, F.data == 'change')
async def cancel_time_hour_change(query: types.CallbackQuery) -> None:
    keyboard: types.InlineKeyboardMarkup = await make_kb_hour()
    await query.message.edit_text(text='Выберите час', reply_markup=keyboard)


@router.callback_query(CreateTaskStates.cancel_time_minute, F.data == 'this')
@router.callback_query(CreateTaskStates.cancel_time_minute, F.data, CheckIntText())
async def cancel_time_minute(query: types.CallbackQuery, state: FSMContext, number: int | None = None) -> None:
    this_datetime = datetime.now()
    minute: int = number or this_datetime.minute
    data: dict = await state.get_data()
    cancel_time = correct_day(day=data['day'], month=data['month'], year=data['year'], hour=data['hour'], minute=minute)
    if cancel_time:
        add_task(user_id=query.from_user.id, title=data['title'], cancel_task=cancel_time, description=data['description'])
    await state.clear()
    await query.message.edit_text(text='Задача поставлена!')
    await query.answer()


@router.callback_query(CreateTaskStates.cancel_time_minute, F.data == 'change')
async def cancel_time_minute_change(query: types.CallbackQuery) -> None:
    keyboard = await make_kb_minute()
    await query.message.edit_text('Выберите минуту', reply_markup=keyboard)

