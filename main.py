import asyncio
import logging

from aiogram import Dispatcher, Bot

from settings import BOT_TOKEN
from storage.models import create_db_tables
from handlers import common_cmd, create_task, inline_mode

# Логирование
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_routers(common_cmd.router, create_task.router, inline_mode.router)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    create_db_tables()
    asyncio.run(main())
