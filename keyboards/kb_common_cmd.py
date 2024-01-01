from aiogram import types

from static import red_cross_emoji, yellow_ticket_emoji


async def kb_main_menu() -> types.InlineKeyboardMarkup:
    buttons: list[list] = [
        [types.InlineKeyboardButton(text='Новая задача', callback_data='create_task')],
        [types.InlineKeyboardButton(text='Мои задачи', callback_data='manage_task')],
        [types.InlineKeyboardButton(text='Справка', callback_data='help')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def kb_back_in_menu() -> types.InlineKeyboardMarkup:
    buttons: list[list] = [
        [types.InlineKeyboardButton(text=f'Вернуться в меню', callback_data='main_menu')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def kb_button_cancel() -> types.InlineKeyboardMarkup:
    buttons: list[list] = [
        [types.InlineKeyboardButton(text=f'{red_cross_emoji}Отмена{red_cross_emoji}', callback_data='cancel')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def kb_button_skip() -> types.InlineKeyboardMarkup:
    buttons: list[list] = [
        [types.InlineKeyboardButton(text='Оставить поле пустым', callback_data='skip')],
        [types.InlineKeyboardButton(text=f'{red_cross_emoji}Отмена{red_cross_emoji}', callback_data='cancel')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
