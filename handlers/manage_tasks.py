from aiogram import F, Router, types, filters

from storage.manage_storage import get_tasks, delete_task, completed_task, in_process_task, check_task_time, failed_task
from storage.models import TaskModel
from keyboards.kb_manage_task import make_kb
import static

router = Router()


async def take_task_id_from_task(callback: types.CallbackQuery) -> int:
    return int(callback.data.split('_')[1])


async def prepare_text_task(task: TaskModel) -> str:
    marks_for_status: dict[str, str] = {
        TaskModel.STATUSES.in_process: static.green_circle_emoji,
        TaskModel.STATUSES.completed: static.blue_circle_emoji,
        TaskModel.STATUSES.failed: static.red_circle_emoji,
        TaskModel.STATUSES.overtime: static.orange_circle_emoji
    }
    text_parts: list[str] = [f'Задача: {static.B_TEXT.format(task.title)}']
    if task.description:
        decs_for_text = f'Описание: {static.I_TEXT.format(task.description)}'
        text_parts.append(decs_for_text)

    deadline_text = f'Дедлайн: {static.B_TEXT.format(task.cancel_task)}'
    text_parts.append(deadline_text)
    text_parts.append(f'Cтатус: {marks_for_status[task.status]}{task.status}')
    return '\n'.join(text_parts)


@router.message(filters.Command('manage'))
async def cmd_manage_tasks(message: types.Message) -> None:
    user_id: int = message.from_user.id
    tasks_list: list[TaskModel] = get_tasks(user_id=user_id)

    if not tasks_list:
        await message.answer('Какие-либо задачи отсутствуют')
        return

    for task in tasks_list:
        if task.status == task.STATUSES.in_process:
            await check_task_time(task=task)
        kb: types.InlineKeyboardMarkup = make_kb(task.task_id, status=task.status)
        text: str = await prepare_text_task(task=task)
        await message.answer(text=text, parse_mode='HTML', reply_markup=kb)


@router.callback_query(F.data.startswith('delete'))
async def query_delete_task(callback: types.CallbackQuery) -> None:
    task_id: int = await take_task_id_from_task(callback=callback)
    delete_task(task_id=task_id)
    await callback.message.edit_text(text='Задача удалена')
    await callback.answer()


@router.callback_query(F.data.startswith('done'))
async def query_done_task(callback: types.CallbackQuery) -> None:
    task_id: int = await take_task_id_from_task(callback=callback)
    completed_task(task_id=task_id)
    await callback.message.edit_text(text='Задача переведена в статус "Выполнена"')
    await callback.answer()


@router.callback_query(F.data.startswith('inProcess'))
async def query_in_process_task(callback: types.CallbackQuery) -> None:
    task_id: int = await take_task_id_from_task(callback=callback)
    in_process_task(task_id=task_id)
    await callback.message.edit_text('Задача переведена в статус "В процессе"')
    await callback.answer()


@router.callback_query(F.data.startswith('failed'))
async def query_failed_task(callback: types.CallbackQuery) -> None:
    task_id: int = await take_task_id_from_task(callback=callback)
    failed_task(task_id=task_id)
    await callback.message.edit_text('Задача переведена в статус "Не выполнена"')
    await callback.answer()
