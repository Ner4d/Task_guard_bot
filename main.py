import os
import asyncio
import logging
import gettext
from pathlib import Path

from aiogram import Dispatcher, Bot
from aiogram.types import bot_command as bc
from aiogram.utils.i18n import I18n

from settings import BOT_TOKEN
from storage.models import create_db_tables
from handlers import common_cmd, create_task, manage_tasks, create_cancel_time, redacting_task, change_tz


# language
BASE_DIR = "/home/oleg/TelegramProjects/Task_guard_bot"
locale_dir = Path(BASE_DIR) / "locale"

i18n = I18n(path=locale_dir, default_locale="en", domain="Task_guard_bot")


# gettext.bindtextdomain('Task_guard_bot', localedir=locale_dir)
# gettext.textdomain('Task_guard_bot')
# gettext.translation('Task_guard_bot', localedir=locale_dir, languages=['en']).install()

# Логирование
logging.basicConfig(level=logging.INFO)

# bot config
bot = Bot(token=BOT_TOKEN)

# dispatcher confi g
dp = Dispatcher()

dp.include_routers(common_cmd.router, manage_tasks.router, create_task.router, create_cancel_time.router,
                   redacting_task.router, change_tz.router)


async def main():
    await bot.set_my_commands(commands=[bc.BotCommand(command='/cancel',
                                                      description='Оптимальный способ завершить задачи и вызвать меню')])
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':

    create_db_tables()
    asyncio.run(main())
