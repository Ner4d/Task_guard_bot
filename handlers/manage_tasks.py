from aiogram import F, Router, types, filters

from storage.manage_storage import get_tasks, delete_task, completed_task
from storage.models import TaskModel
from keyboards.manage_task import make_kb

router = Router()

EM_TEXT = '<em>{}</em>'  # Подчеркнутый текст
I_TEXT = '<i>{}</i>'  # Курсив
B_TEXT = '<strong>{}</strong>'  # Жирный текст

green_circle_emoji = '\U0001F7E2'
red_circle_emoji = '\U0001F534'
blue_circle_emoji = '\U0001F535'


async def prepare_text_task(task: TaskModel) -> str:
    marks_for_status: dict[str, str] = {
        'В процессе': green_circle_emoji,
        'Выполнена': blue_circle_emoji,
        'Не выполнена': red_circle_emoji
    }
    text_parts: list[str] = [f'Задача: {EM_TEXT.format(task.title)}']
    if task.description:
        decs_for_text = f'Описание: {I_TEXT.format(task.description)}'
        text_parts.append(decs_for_text)

    deadline_text = f'Дедлайн: {B_TEXT.format(task.cancel_task)}'
    text_parts.append(deadline_text)
    text_parts.append(f'Cтатус: {marks_for_status[task.status]}{task.status}')
    return '\n'.join(text_parts)


@router.message(filters.Command('manage'))
async def cmd_manage_tasks(message: types.Message) -> None:
    user_id: int = message.from_user.id
    tasks_list: list[TaskModel] = get_tasks(user_id=user_id)

    for task in tasks_list:
        kb: types.InlineKeyboardMarkup = make_kb(task.task_id)
        text: str = await prepare_text_task(task=task)
        await message.answer(text=text, parse_mode='HTML', reply_markup=kb)


@router.callback_query(F.data.startswith('delete'))
async def query_delete_task(callback: types.CallbackQuery) -> None:
    task_id: int = int(callback.data.split('_')[1])
    delete_task(task_id=task_id)
    await callback.message.edit_text(text='Задача удалена')
    await callback.answer()


@router.callback_query(F.data.startswith('done'))
async def query_done_task(callback: types.CallbackQuery) -> None:
    task_id: int = int(callback.data.split('_')[1])
    completed_task(task_id=task_id)
    await callback.message.edit_text(text='Задача обновлена')
    await callback.answer()
