import environ
import os


env = environ.Env()

BASE_DIR: str = os.getcwd()

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Конфигурация бота
BOT_TOKEN = env('BOT_TOKEN')