from datetime import datetime

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

month_list = [
    'Январь',
    'Февраль',
    'Март',
    'Апрель',
    'Май',
    'Июнь',
    'Июль',
    'Август',
    'Сентябрь',
    'Октябрь',
    'Ноябрь',
    'Декабрь',
]


async def make_kb_change_default() -> types.InlineKeyboardMarkup:
    buttons: list[list] = [
        [types.InlineKeyboardButton(text='По умолчанию', callback_data='default_time')],
        [types.InlineKeyboardButton(text='Изменить', callback_data='change_datetime')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def make_kb_change_unit() -> types.InlineKeyboardMarkup:
    buttons: list[list] = [
        [types.InlineKeyboardButton(text='Подтвердить', callback_data='this')],
        [types.InlineKeyboardButton(text='Изменить', callback_data='change')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def make_kb_days() -> types.InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for button_index in range(1, 32):
        str_index = str(button_index)
        if len(str_index) == 1:
            str_index = '0' + str_index
        kb_builder.add(types.InlineKeyboardButton(text=str_index, callback_data=str_index))
        kb_builder.adjust(7)
    return kb_builder.as_markup()


async def make_kb_month() -> types.InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for button_index in range(12):
        str_index = str(button_index + 1)
        month: str = month_list[button_index]
        kb_builder.add(types.InlineKeyboardButton(text=month, callback_data=str_index))
    kb_builder.adjust(4)
    return kb_builder.as_markup()


async def make_kb_year() -> types.InlineKeyboardMarkup:
    year: int = datetime.now().year
    kb_builder = InlineKeyboardBuilder()
    for year_index in range(year, year + 12):
        str_year = str(year_index)
        kb_builder.add(types.InlineKeyboardButton(text=str_year, callback_data=str_year))
    kb_builder.adjust(4)
    return kb_builder.as_markup()


async def make_kb_hour() -> types.InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for hour in range(24):
        str_hour = str(hour)
        kb_builder.add(types.InlineKeyboardButton(text=str_hour, callback_data=str_hour))
    kb_builder.adjust(6)
    return kb_builder.as_markup()


async def make_kb_minute() -> types.InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for minute in range(12):
        minute *= 5
        str_minute = str(minute)
        if len(str_minute) == 1:
            str_minute = '0' + str_minute
        kb_builder.add(types.InlineKeyboardButton(text=str_minute, callback_data=str_minute))
    kb_builder.adjust(4)
    return kb_builder.as_markup()


async def make_kb_result() -> types.InlineKeyboardMarkup:
    buttons: list[list] = [
        [types.InlineKeyboardButton(text='Сохранить', callback_data='save')],
        [types.InlineKeyboardButton(text='Изменить название', callback_data='redact_title')],
        [types.InlineKeyboardButton(text='Изменить описание', callback_data='redact_description')],
        [types.InlineKeyboardButton(text='Изменить крайний срок', callback_data='redact_datetime')],
        [types.InlineKeyboardButton(text='Отмена', callback_data='cancel')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
