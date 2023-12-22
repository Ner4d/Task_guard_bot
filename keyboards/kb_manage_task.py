from aiogram import types

from storage.models import TaskModel


def make_kb(task_id: int, status: str) -> types.InlineKeyboardMarkup:
    task_id = str(task_id)
    buttons_row: list = [types.InlineKeyboardButton(text='Удалить', callback_data=f'delete_{task_id}')]

    if status == TaskModel.STATUSES.completed:
        buttons_row.append(types.InlineKeyboardButton(text='Ещё в процессе', callback_data=f'inProcess_{task_id}'))
        buttons_row.append(types.InlineKeyboardButton(text='Не выполнена', callback_data=f'failed_{task_id}'))
    elif status == TaskModel.STATUSES.in_process:
        buttons_row.append(types.InlineKeyboardButton(text='Завершить', callback_data=f'done_{task_id}'))
        buttons_row.append(types.InlineKeyboardButton(text='Не выполнена', callback_data=f'failed_{task_id}'))
    else:  # Я предполагаю что в оставшихся варианта она либо в статусе "Не завершена", либо "Просрочена"
        buttons_row.append(types.InlineKeyboardButton(text='Завершить', callback_data=f'done_{task_id}'))
        buttons_row.append(types.InlineKeyboardButton(text='Не выполнена', callback_data=f'failed_{task_id}'))

    buttons_column: list[list[types.InlineKeyboardButton]] = [buttons_row]

    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons_column)
    return inline_keyboard
