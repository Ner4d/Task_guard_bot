import gettext
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


# Локализация

LOCALES_DIR = path.join(BASE_DIR, 'locales')

lang = 'en'

gettext.bindtextdomain(domain=lang, localedir=LOCALES_DIR)
gettext.textdomain(lang)
lang_pack = gettext.translation(domain=lang, localedir=LOCALES_DIR)

