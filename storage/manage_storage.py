from gettext import gettext as _

import asyncio

from aiogram import Bot
from datetime import datetime, timedelta, timezone
from random import randint

from storage.models import UserModel, TaskModel


async def check_burn_task(_bot: Bot):
    while True:
        query_task = (TaskModel.select(TaskModel, UserModel).join(UserModel))
        for task in query_task:
            now_user_time = datetime.now() + timedelta(hours=task.owner.time_zone)
            if now_user_time < task.cancel_task and task.status == TaskModel.STATUSES.in_process:
                lost_time_minute = (task.cancel_task - now_user_time).seconds // 60
                if lost_time_minute <= 5:
                    text = _('Уважаемый пользовать, у вас сроки горят, задача {}').format(task.title)
                    await _bot.send_message(chat_id=task.owner.user_id, text=text)
        await asyncio.sleep(300)


async def change_tz_user(user_id: int, new_tz: int) -> None:
    if not UserModel.select().where(UserModel.user_id == user_id):
        user = await add_user(user_id=user_id)
    else:
        user = UserModel.get(UserModel.user_id == user_id)
    user.time_zone = new_tz
    user.save()


async def get_user_tz(user_id: int) -> int:
    if not UserModel.select().where(UserModel.user_id == user_id):
        user = await add_user(user_id=user_id)
    else:
        user = UserModel.get(UserModel.user_id == user_id)
    return user.time_zone


async def add_user(user_id: int) -> UserModel:
    user = UserModel.create(user_id=user_id)
    user.save()
    return user


async def change_language(user_id: int) -> str:
    if not UserModel.select().where(UserModel.user_id == user_id):
        user = await add_user(user_id=user_id)
    else:
        user = UserModel.get(UserModel.user_id == user_id)
    table_change = {
        'en': 'ru',
        'ru': 'en',
    }
    user.language = table_change[user.language]
    user.save()
    return user.language


async def add_task(user_id: int, title: str, cancel_task: datetime, description: None | str) -> None:
    if not UserModel.select().where(UserModel.user_id == user_id):
        owner = await add_user(user_id=user_id)
    else:
        owner: UserModel = UserModel.get(UserModel.user_id == user_id)
    task_id: int = randint(10**6, (10**8)-1)
    sort_time = cancel_task.timestamp()
    TaskModel.create(owner=owner, task_id=task_id, title=title, cancel_task=cancel_task, description=description,
                     sort_time=sort_time).save()
    return


async def get_tasks(user_id: int) -> list:
    if not UserModel.select().where(UserModel.user_id == user_id):
        owner = await add_user(user_id=user_id)
    else:
        owner: UserModel = UserModel.get(UserModel.user_id == user_id)
    return TaskModel.select().where(TaskModel.owner == owner).order_by('sort_time')


async def completed_task(task_id: int) -> None:
    task: TaskModel = TaskModel.get(TaskModel.task_id == task_id)
    task.status = task.STATUSES.completed
    task.save()
    return


async def in_process_task(task_id: int) -> None:
    task: TaskModel = TaskModel.get(TaskModel.task_id == task_id)
    task.status = task.STATUSES.in_process
    task.save()
    return


async def failed_task(task_id: int) -> None:
    task: TaskModel = TaskModel.get(TaskModel.task_id == task_id)
    task.status = task.STATUSES.failed
    task.save()
    return


async def check_task_time(task: TaskModel, user_id: int) -> None:
    user: UserModel = UserModel.get(UserModel.user_id == user_id)
    now_time = datetime.now() + timedelta(hours=user.time_zone)
    if task.cancel_task <= now_time:
        task.status = TaskModel.STATUSES.overtime
        task.save()
    return


async def delete_task(task_id: int) -> None:
    task: TaskModel = TaskModel.get(TaskModel.task_id == task_id)
    task.delete_instance()
    return
