from gettext import gettext as _

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def kb_inline_main_menu() -> types.InlineKeyboardMarkup:
    buttons: list[list] = [
        [types.InlineKeyboardButton(text=_('Новая задача'), callback_data='create_task')],
        [types.InlineKeyboardButton(text=_('Мои задачи'), callback_data='manage_task')],
        [types.InlineKeyboardButton(text=_('Справка'), callback_data='help')],
        [types.InlineKeyboardButton(text=_('Изменить часовой пояс'), callback_data='change_timezone')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def kb_inline_back_in_menu() -> types.InlineKeyboardMarkup:
    buttons: list[list] = [
        [types.InlineKeyboardButton(text=_('Вернуться в меню'), callback_data='main_menu')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def kb_inline_button_cancel() -> types.InlineKeyboardMarkup:
    buttons: list[list] = [
        [types.InlineKeyboardButton(text=_('Отмена'), callback_data='cancel')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def kb_button_cancel() -> types.ReplyKeyboardMarkup:
    buttons: list[list] = [
        [types.KeyboardButton(text='/cancel')],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard


async def kb_inline_button_skip() -> types.InlineKeyboardMarkup:
    buttons: list[list] = [
        [types.InlineKeyboardButton(text=_('Оставить поле пустым'), callback_data='skip')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def kb_inline_timezone_russia() -> types.InlineKeyboardMarkup:
    #  Значения ключей расчитаны на Московское время
    city_timezone = {
        'Калининград UTC+2': '-1',
        'Москва UTC+3': '0',
        'Самара UTC+4': '1',
        'Пермь UTC+5': '2',
        'Омск UTC+6': '3',
        'Алтай UTC+7': '4',
        'Иркутск UTC+8': '5',
        'Забайкальский край UTC+9': '6',
        'Приморский край UTC+10': '7',
        'Магадан UTC+11': '8',
        'Камчатка UTC+12': '9',
    }
    kb_builder = InlineKeyboardBuilder()
    for city, timezone in city_timezone.items():
        kb_builder.add(types.InlineKeyboardButton(text=_(city), callback_data=timezone))
    kb_builder.adjust(2)
    return kb_builder.as_markup()
