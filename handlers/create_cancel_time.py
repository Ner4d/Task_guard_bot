from datetime import datetime, timedelta
from gettext import gettext as _

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from filters import CheckIntText, correct_day
from handlers.redacting_task import prepare_text_to_result
from handlers.states import CreateTaskStates, RedactingTaskStates
from keyboards.kb_cancel_time import (make_kb_change_unit, make_kb_days,
                                      make_kb_hour, make_kb_minute,
                                      make_kb_month, make_kb_result,
                                      make_kb_year, month_list)
from keyboards.kb_common_cmd import kb_inline_main_menu
from static.font_styles import B_TEXT
from storage.manage_storage import add_task

router = Router()


@router.callback_query(F.data == 'save')
async def save_result_task(query: types.CallbackQuery, state: FSMContext) -> None:
    keyboard = await kb_inline_main_menu()
    data: dict = await state.get_data()
    user_id: int = query.from_user.id
    await add_task(user_id=user_id, title=data['title'], cancel_task=data['cancel_time'],
                   description=data['description'])
    await state.clear()
    await query.message.edit_text(text=_('Задача готова!'), reply_markup=keyboard)


@router.callback_query(RedactingTaskStates.redact_result, F.data == 'this')
@router.callback_query(CreateTaskStates.create_cancel_time, F.data == 'default_time')
async def default_time(query: types.CallbackQuery, state: FSMContext) -> None:
    keyboard = await make_kb_result()
    data: dict = await state.get_data()
    state_name = await state.get_state()
    if state_name == CreateTaskStates.create_cancel_time:
        cancel_time = datetime.now() + timedelta(days=1, hours=data.get('user_tz', 0))
    else:
        cancel_time = datetime(day=data['day'], month=data['month'], year=data['year'], hour=data['hour'],
                               minute=data['minute'])
    await state.update_data(cancel_time=cancel_time)
    text = await prepare_text_to_result(title=data['title'], description=data['description'], cancel_time=cancel_time)
    await query.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
    await state.set_state()
    await query.answer()


@router.callback_query(F.data == 'redact_datetime')
@router.callback_query(CreateTaskStates.create_cancel_time, F.data == 'change_datetime')
async def create_cancel_time(query: types.CallbackQuery, state: FSMContext) -> None:
    keyboard: types.InlineKeyboardMarkup = await make_kb_change_unit()
    user_tz: int = (await state.get_data()).get('user_tz', 0)
    if query.data == 'change_datetime':
        await state.set_state(CreateTaskStates.cancel_time_day)
    else:  # query.data == 'redact_date'
        await state.set_state(RedactingTaskStates.redact_date_day)
    this_day = datetime.now() + timedelta(hours=user_tz)
    await query.message.edit_text(text=_('Выбрать текущий день: {}').format(B_TEXT.format(this_day.day)),
                                  reply_markup=keyboard,
                                  parse_mode='HTML')


@router.callback_query(CreateTaskStates.cancel_time_day, F.data == 'change')
@router.callback_query(RedactingTaskStates.redact_date_day, F.data == 'change')
async def cancel_time_day_change(query: types.CallbackQuery) -> None:
    keyboard: types.InlineKeyboardMarkup = await make_kb_days()
    await query.message.edit_text(text=_('Выберите день'), reply_markup=keyboard)


@router.callback_query(RedactingTaskStates.redact_date_day, F.data == 'this')
@router.callback_query(RedactingTaskStates.redact_date_day, F.data, CheckIntText())
@router.callback_query(CreateTaskStates.cancel_time_day, F.data == 'this')
@router.callback_query(CreateTaskStates.cancel_time_day, F.data, CheckIntText())
async def cancel_time_day(query: types.CallbackQuery, state: FSMContext, number: int | None = None) -> None:
    state_name: str = await state.get_state()
    user_tz: int = (await state.get_data()).get('user_tz', 0)
    if state_name == CreateTaskStates.cancel_time_day:
        await state.set_state(CreateTaskStates.cancel_time_month)
    else:
        await state.set_state(RedactingTaskStates.redact_date_month)
    this_datetime = datetime.now() + timedelta(hours=user_tz)
    this_month: str = month_list[this_datetime.month - 1]
    keyboard: types.InlineKeyboardMarkup = await make_kb_change_unit()
    day: int = number or this_datetime.day
    await state.update_data(day=day)
    await query.message.edit_text(text=_('Выбрать текущий месяц: {}').format(B_TEXT.format(this_month)),
                                  reply_markup=keyboard,
                                  parse_mode='HTML')


@router.callback_query(RedactingTaskStates.redact_date_month, F.data == 'change')
@router.callback_query(CreateTaskStates.cancel_time_month, F.data == 'change')
async def cancel_time_month_change(query: types.CallbackQuery) -> None:
    keyboard: types.InlineKeyboardMarkup = await make_kb_month()
    await query.message.edit_text(text=_('Выберите месяц'), reply_markup=keyboard)


@router.callback_query(RedactingTaskStates.redact_date_month, F.data == 'this')
@router.callback_query(RedactingTaskStates.redact_date_month, F.data, CheckIntText())
@router.callback_query(CreateTaskStates.cancel_time_month, F.data == 'this')
@router.callback_query(CreateTaskStates.cancel_time_month, F.data, CheckIntText())
async def cancel_time_month(query: types.CallbackQuery, state: FSMContext, number: int | None = None) -> None:
    keyboard: types.InlineKeyboardMarkup = await make_kb_change_unit()
    user_tz: int = (await state.get_data()).get('user_tz', 0)
    this_datetime = datetime.now() + timedelta(hours=user_tz)
    month: int = number or this_datetime.month
    state_name: str = await state.get_state()
    await state.update_data(month=month)
    if state_name == CreateTaskStates.cancel_time_month:
        await state.set_state(CreateTaskStates.cancel_time_year)
    else:
        await state.set_state(RedactingTaskStates.redact_date_year)
    await query.message.edit_text(text=_('Выбрать текущий год: {}').format(B_TEXT.format(this_datetime.year)),
                                  reply_markup=keyboard,
                                  parse_mode='HTML')


@router.callback_query(RedactingTaskStates.redact_date_year, F.data == 'change')
@router.callback_query(CreateTaskStates.cancel_time_year, F.data == 'change')
async def cancel_time_year_change(query: types.CallbackQuery) -> None:
    keyboard: types.InlineKeyboardMarkup = await make_kb_year()
    await query.message.edit_text(text=_('Выберите год'), reply_markup=keyboard)


@router.callback_query(RedactingTaskStates.redact_date_year, F.data == 'this')
@router.callback_query(CreateTaskStates.cancel_time_year, F.data == 'this')
@router.callback_query(RedactingTaskStates.redact_date_year, F.data, CheckIntText())
@router.callback_query(CreateTaskStates.cancel_time_year, F.data, CheckIntText())
async def cancel_time_year(query: types.CallbackQuery, state: FSMContext, number: int | None = None) -> None:
    keyboard: types.InlineKeyboardMarkup = await make_kb_change_unit()
    user_tz: int = (await state.get_data()).get('user_tz', 0)
    this_datetime = datetime.now() + timedelta(hours=user_tz)
    year: int = number or this_datetime.year
    await state.update_data(year=year)
    state_name = await state.get_state()
    if state_name == CreateTaskStates.cancel_time_year:
        await state.set_state(CreateTaskStates.cancel_time_hour)
    else:  # state_name == RedactingTaskStates.redact_date_year
        await state.set_state(RedactingTaskStates.redact_time_hour)
    await query.message.edit_text(text=_('Выбрать текущий час: {}').format(B_TEXT.format(this_datetime.hour)),
                                  reply_markup=keyboard,
                                  parse_mode='HTML')


@router.callback_query(RedactingTaskStates.redact_time_hour, F.data == 'change')
@router.callback_query(CreateTaskStates.cancel_time_hour, F.data == 'change')
async def cancel_time_hour_change(query: types.CallbackQuery) -> None:
    keyboard: types.InlineKeyboardMarkup = await make_kb_hour()
    await query.message.edit_text(text=_('Выберите час'), reply_markup=keyboard)


@router.callback_query(RedactingTaskStates.redact_time_hour, F.data == 'this')
@router.callback_query(CreateTaskStates.cancel_time_hour, F.data == 'this')
@router.callback_query(RedactingTaskStates.redact_time_hour, F.data, CheckIntText())
@router.callback_query(CreateTaskStates.cancel_time_hour, F.data, CheckIntText())
async def cancel_time_hour(query: types.CallbackQuery, state: FSMContext, number: int | None = None) -> None:
    keyboard: types.InlineKeyboardMarkup = await make_kb_change_unit()
    user_tz: int = (await state.get_data()).get('user_tz', 0)
    this_datetime = datetime.now() + timedelta(hours=user_tz)
    hour: int = number or this_datetime.hour
    await state.update_data(hour=hour)
    state_name = await state.get_state()
    if state_name == CreateTaskStates.cancel_time_hour:
        await state.set_state(CreateTaskStates.cancel_time_minute)
    else:
        await state.set_state(RedactingTaskStates.redact_time_minute)
    await query.message.edit_text(text=_('Выбрать текущую минуту: {}').format(B_TEXT.format(this_datetime.minute)),
                                  reply_markup=keyboard,
                                  parse_mode='HTML')


@router.callback_query(RedactingTaskStates.redact_time_minute, F.data == 'change')
@router.callback_query(CreateTaskStates.cancel_time_minute, F.data == 'change')
async def cancel_time_minute_change(query: types.CallbackQuery) -> None:
    keyboard = await make_kb_minute()
    await query.message.edit_text(_('Выберите минуту'), reply_markup=keyboard)


@router.callback_query(RedactingTaskStates.redact_time_minute, F.data == 'this')
@router.callback_query(CreateTaskStates.cancel_time_minute, F.data == 'this')
@router.callback_query(RedactingTaskStates.redact_time_minute, F.data, CheckIntText())
@router.callback_query(CreateTaskStates.cancel_time_minute, F.data, CheckIntText())
async def cancel_time_minute(query: types.CallbackQuery, state: FSMContext, number: int | None = None) -> None:
    keyboard = await make_kb_result()
    data: dict = await state.get_data()
    this_datetime = datetime.now() + timedelta(hours=data.get('user_tz', 0))
    minute: int = number or this_datetime.minute
    day = correct_day(day=data['day'], month=data['month'], year=data['year'])
    cancel_time = datetime(day=day, month=data['month'], year=data['year'], hour=data['hour'], minute=minute)
    await state.update_data(cancel_time=cancel_time)
    text: str = await prepare_text_to_result(title=data['title'], cancel_time=cancel_time,
                                             description=data['description'])
    await state.set_state()
    await query.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
    await query.answer()
