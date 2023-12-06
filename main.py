import asyncio
import logging

from aiogram import Dispatcher, Bot

from settings import BOT_TOKEN

# Логирование
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
