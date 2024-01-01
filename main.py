import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.types import bot_command as bc

from settings import BOT_TOKEN
from storage.models import create_db_tables
from handlers import common_cmd, create_task, manage_tasks, create_cancel_time, redacting_task

# Логирование
logging.basicConfig(level=logging.INFO)

# bot config
bot = Bot(token=BOT_TOKEN)

# dispatcher confi g
dp = Dispatcher()
dp.include_routers(common_cmd.router, manage_tasks.router, create_task.router, create_cancel_time.router,
                   redacting_task.router)


async def main():
    await bot.set_my_commands(commands=[bc.BotCommand(command='/cancel',
                                                      description='Оптимальный способ завершить задачи и вызвать меню')])
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    create_db_tables()
    asyncio.run(main())
