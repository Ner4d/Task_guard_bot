from gettext import gettext as _

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from storage.models import TaskModel


async def make_kb(task_id: int, status: str) -> types.InlineKeyboardMarkup:
    text_button_in_process = _('Ещё в процессе')
    text_button_delete = _('Удалить')
    text_button_failed = _('Не выполнена')
    text_button_done = _('Завершить')
    task_id = str(task_id)
    buttons_row: list = [types.InlineKeyboardButton(text=text_button_delete, callback_data=f'delete_{task_id}')]

    if status == TaskModel.STATUSES.completed:
        buttons_row.append(types.InlineKeyboardButton(text=text_button_in_process,
                                                      callback_data=f'inProcess_{task_id}'))
        buttons_row.append(types.InlineKeyboardButton(text=text_button_failed, callback_data=f'failed_{task_id}'))
    elif status in (TaskModel.STATUSES.in_process, TaskModel.STATUSES.overtime):
        buttons_row.append(types.InlineKeyboardButton(text=text_button_done, callback_data=f'done_{task_id}'))
        buttons_row.append(types.InlineKeyboardButton(text=text_button_failed, callback_data=f'failed_{task_id}'))
    else:  # Я предполагаю что в оставшихся варианта задача будет в статусе "Не завершена"
        buttons_row.append(types.InlineKeyboardButton(text=text_button_done, callback_data=f'done_{task_id}'))
        buttons_row.append(types.InlineKeyboardButton(text=text_button_in_process,
                                                      callback_data=f'inProcess_{task_id}'))

    buttons_column: list[list[types.InlineKeyboardButton]] = [buttons_row]

    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons_column)
    return inline_keyboard


async def make_kb_end(task_id: int, status: str, max_page: int, page_num: int = 1) -> types.InlineKeyboardMarkup:
    base_kb = await make_kb(task_id=task_id, status=status)
    kb_builder = InlineKeyboardBuilder.from_markup(base_kb)
    if page_num == 1:
        kb_builder.add(
            types.InlineKeyboardButton(text=f'{page_num}/{max_page}', callback_data='current'),
            types.InlineKeyboardButton(text=_('Следующая'), callback_data='next'),
        )
    else:  # page_num == max_page
        kb_builder.add(
            types.InlineKeyboardButton(text=f'{page_num}/{max_page}', callback_data='current'),
        )
    kb_builder.adjust(3)
    return kb_builder.as_markup()
