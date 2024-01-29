from collections import namedtuple
from datetime import datetime

from peewee import (CharField, DateTimeField, ForeignKeyField, IntegerField,
                    Model, TextField)

from settings import DATA_BASE


# Базовая модель с настроенным подключением к конкретной базе данных для последующих моделей
class BaseModel(Model):

    class Meta:
        database = DATA_BASE


# Модель для связи пользователя с только его задачами
class UserModel(BaseModel):
    user_id = IntegerField(unique=True)
    language = CharField(default='ru')
    time_zone = IntegerField(default=0)


# Сама модель задач с необходимыми данными
class TaskModel(BaseModel):
    owner = ForeignKeyField(UserModel, backref='tasks')
    task_id = IntegerField(unique=True)
    title = CharField()
    description = TextField(null=True)

    start_task = DateTimeField(default=datetime.now)
    cancel_task = DateTimeField()
    sort_time = IntegerField()

    # Status
    status = namedtuple('status', ['in_process', 'failed', 'completed', 'overtime'])
    STATUSES = status('В процессе', 'Не выполнена', 'Выполнена', 'Просрочена')
    status = CharField(default=STATUSES.in_process)


def create_db_tables():
    with DATA_BASE:
        DATA_BASE.create_tables([UserModel, TaskModel])
