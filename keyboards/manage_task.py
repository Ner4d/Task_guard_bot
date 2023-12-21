from aiogram import types


def make_kb(task_id: int) -> types.InlineKeyboardMarkup:
    task_id = str(task_id)
    buttons: list[list] = [
        [types.InlineKeyboardButton(text='Удалить', callback_data=f'delete_{task_id}')],
        [types.InlineKeyboardButton(text='Завершить', callback_data=f'done_{task_id}')],
    ]
    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_keyboard
green_circle_emoji = '\U0001F7E2'
red_circle_emoji = '\U0001F534'
blue_circle_emoji = '\U0001F535'