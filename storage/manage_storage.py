from datetime import datetime
from random import randint

from storage.models import UserModel, TaskModel


def add_user(user_id: int) -> None:
    UserModel.create(user_id=user_id).save()
    return


def add_task(user_id: int, title: str, cancel_task: datetime, description: None | str = None) -> None:
    if not UserModel.select().where(UserModel.user_id == user_id):
        add_user(user_id=user_id)
    owner: UserModel = UserModel.get(UserModel.user_id == user_id)
    task_id: int = randint(10**6, (10**8)-1)
    TaskModel.create(owner=owner, task_id=task_id, title=title, cancel_task=cancel_task, description=description).save()
    return


def get_tasks(user_id: int) -> list:
    if not UserModel.select().where(UserModel.user_id == user_id):
        add_user(user_id=user_id)
    owner: UserModel = UserModel.get(UserModel.user_id == user_id)
    return TaskModel.select().where(TaskModel.owner == owner)


def completed_task(task_id: int) -> None:
    task: TaskModel = TaskModel.get(TaskModel.task_id == task_id)
    task.status = task.STATUSES.completed
    task.save()
    return


def in_process_task(task_id: int) -> None:
    task: TaskModel = TaskModel.get(TaskModel.task_id == task_id)
    task.status = task.STATUSES.in_process
    task.save()
    return


def failed_task(task_id: int) -> None:
    task: TaskModel = TaskModel.get(TaskModel.task_id == task_id)
    task.status = task.STATUSES.failed
    task.save()
    return


async def check_task_time(task: TaskModel) -> None:
    if task.cancel_task <= datetime.now():
        task.status = task.STATUSES.overtime
        task.save()
    return


def delete_task(task_id: int) -> None:
    task: TaskModel = TaskModel.get(TaskModel.task_id == task_id)
    task.delete_instance()
    return
