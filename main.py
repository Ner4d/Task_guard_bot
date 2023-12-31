import asyncio
import logging

from aiogram import Dispatcher, Bot

from settings import BOT_TOKEN
from storage.models import create_db_tables
from handlers import common_cmd, create_task, manage_tasks, create_cancel_time

# Логирование
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_routers(common_cmd.router, manage_tasks.router, create_task.router, create_cancel_time.router)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    create_db_tables()
    asyncio.run(main())
