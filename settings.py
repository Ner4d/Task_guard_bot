import environ
from os import getcwd, path
from peewee import SqliteDatabase


env = environ.Env()

BASE_DIR: str = getcwd()

environ.Env.read_env(path.join(BASE_DIR, '.env'))

# Конфигурация бота
BOT_TOKEN = env('BOT_TOKEN')

# Конфигурация базы данных
DATA_BASE = SqliteDatabase('DataBaseSQLite.db')
