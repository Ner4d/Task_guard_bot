from peewee import Model, IntegerField, CharField, ForeignKeyField, TextField, DateTimeField

from settings import DATA_BASE
from datetime import datetime
from collections import namedtuple


# Базовая модель с настроенным подключением к конкретной базе данных для последующих моделей
class BaseModel(Model):

    class Meta:
        database = DATA_BASE


# Модель для связи пользователя с только его задачами
class UserModel(BaseModel):
    user_id = IntegerField(unique=True)


# Сама модель задач с необходимыми данными
class TaskModel(BaseModel):
    owner = ForeignKeyField(UserModel, backref='tasks')
    task_id = IntegerField(unique=True)
    title = CharField()
    description = TextField(null=True)
    start_task = DateTimeField(default=datetime.now)
    cancel_task = DateTimeField()

    # Status
    status = namedtuple('status', ['created', 'in_process', 'failed', 'completed'])
    STATUSES = status('Создана', 'В процессе', 'Не выполнена', 'Выполнена')
    status = CharField(default=STATUSES.in_process)


def create_db_tables():
    with DATA_BASE:
        DATA_BASE.create_tables([UserModel, TaskModel])
