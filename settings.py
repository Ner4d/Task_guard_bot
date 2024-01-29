from os import getcwd, path

import environ
from peewee import SqliteDatabase

env = environ.Env()

BASE_DIR: str = getcwd()

environ.Env.read_env(path.join(BASE_DIR, '.env'))

# Конфигурация бота
BOT_TOKEN = env('BOT_TOKEN')

# Конфигурация базы данных
DATA_BASE = SqliteDatabase('DataBaseSQLite.db')


# Локализация

LOCALES_DIR = path.join(BASE_DIR, 'locale')
