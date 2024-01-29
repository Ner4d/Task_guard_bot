from gettext import gettext as _
from math import ceil

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

import static
from keyboards.kb_cancel_time import month_list
from keyboards.kb_common_cmd import kb_inline_back_in_menu
from keyboards.kb_manage_task import make_kb, make_kb_end
from storage.manage_storage import (check_task_time, completed_task,
                                    delete_task, failed_task, get_tasks,
                                    in_process_task)
from storage.models import TaskModel

router = Router()


async def take_task_id_from_task(callback: types.CallbackQuery) -> int:
    return int(callback.data.split('_')[1])


async def prepare_text_task(task: TaskModel | int) -> str:
    """
    :param task: Может быть как самим объектом, так и его id
    :return:
    """
    if not isinstance(task, TaskModel):
        task = TaskModel.get(TaskModel.task_id == task)

    if task.status == TaskModel.STATUSES.in_process:
        await check_task_time(task=task)

    marks_for_status: dict[str, str] = {
        TaskModel.STATUSES.in_process: static.green_circle_emoji,
        TaskModel.STATUSES.completed: static.blue_circle_emoji,
        TaskModel.STATUSES.failed: static.red_circle_emoji,
        TaskModel.STATUSES.overtime: static.orange_circle_emoji
    }

    text_parts: list[str] = [_('Задача: {}').format(static.B_TEXT.format(task.title))]

    if task.description:
        decs_for_text = _('Описание: {}').format(static.I_TEXT.format(task.description))
        text_parts.append(decs_for_text)

    month = task.cancel_task.month
    cancel_time_format = task.cancel_task.strftime('%d {} %Y - %H:%M').format(month_list[month])
    deadline_text = _('Крайний срок: {}').format(static.B_TEXT.format(cancel_time_format))
    text_parts.append(deadline_text)
    text_parts.append(_('Cтатус: {}{}').format(marks_for_status[task.status], _(task.status)))
    return '\n'.join(text_parts)


@router.callback_query(F.data == 'manage_task')
async def cmd_manage_tasks(query: types.CallbackQuery, state: FSMContext) -> None:
    user_id: int = query.from_user.id
    tasks_list: list[TaskModel] = await get_tasks(user_id=user_id)
    if not tasks_list:
        keyboard = await kb_inline_back_in_menu()
        await query.message.edit_text(text=_('Какие-либо задачи отсутствуют'), reply_markup=keyboard)
        return
    start_index = 0
    end_index: int = 4
    max_num_page: int = ceil(len(tasks_list) / 4)
    await state.update_data(num_page=1, max_num_page=max_num_page, start_index=start_index)
    await query.message.delete()

    for index, task in enumerate(tasks_list[:end_index]):

        if task.status == task.STATUSES.in_process:
            await check_task_time(task=task, user_id=query.from_user.id)

        kb: types.InlineKeyboardMarkup = await make_kb(task_id=task.task_id, status=task.status)
        text: str = await prepare_text_task(task=task)

        if index == 3 and max_num_page > 1:
            kb = await make_kb_end(task_id=task.task_id, status=task.status, max_page=max_num_page)

        await query.message.answer(text=text, parse_mode='HTML', reply_markup=kb)
        await query.answer()


@router.callback_query(F.data == 'next')
async def button_next_page(query: types.CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    data = await state.get_data()
    num_page = data['num_page'] + 1
    await state.update_data(num_page=num_page)
    max_num_page = data['max_num_page']
    start_index = data['start_index'] + 4
    await state.update_data(start_index=start_index)
    end_index = start_index + 4
    user_id: int = query.from_user.id
    tasks_list: list[TaskModel] = await get_tasks(user_id=user_id)
    current_page = tasks_list[start_index:end_index]
    for index, task in enumerate(current_page):
        if task.status == task.STATUSES.in_process:
            await check_task_time(task=task)
        kb: types.InlineKeyboardMarkup = await make_kb(task_id=task.task_id, status=task.status)
        text: str = await prepare_text_task(task=task)

        if index == (len(current_page) - 1):
            kb = await make_kb_end(task_id=task.task_id, status=task.status, max_page=max_num_page, page_num=num_page)

        await query.message.answer(text=text, parse_mode='HTML', reply_markup=kb)
        await query.answer()


@router.callback_query(F.data.startswith('delete'))
async def query_delete_task(callback: types.CallbackQuery) -> None:
    task_id: int = await take_task_id_from_task(callback=callback)
    await delete_task(task_id=task_id)
    await callback.message.edit_text(text=_('Задача удалена'))


@router.callback_query(F.data.startswith('done'))
async def query_done_task(callback: types.CallbackQuery) -> None:
    task_id: int = await take_task_id_from_task(callback=callback)
    await completed_task(task_id=task_id)

    text: str = await prepare_text_task(task=task_id)
    kb = await make_kb(task_id=task_id, status=TaskModel.STATUSES.completed)

    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode='HTML')


@router.callback_query(F.data.startswith('inProcess'))
async def query_in_process_task(callback: types.CallbackQuery) -> None:
    task_id: int = await take_task_id_from_task(callback=callback)
    await in_process_task(task_id=task_id)

    kb = await make_kb(task_id=task_id, status=TaskModel.STATUSES.in_process)
    text: str = await prepare_text_task(task=task_id)

    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode='HTML')


@router.callback_query(F.data.startswith('failed'))
async def query_failed_task(callback: types.CallbackQuery) -> None:
    task_id: int = await take_task_id_from_task(callback=callback)
    await failed_task(task_id=task_id)

    text: str = await prepare_text_task(task=task_id)
    kb = await make_kb(task_id=task_id, status=TaskModel.STATUSES.failed)

    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode='HTML')
