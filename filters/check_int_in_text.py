from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message


class CheckIntText(BaseFilter):
    async def __call__(self, query_message: CallbackQuery | Message) -> bool | dict:
        text = query_message.data if isinstance(query_message, CallbackQuery) else query_message.text
        try:
            number = int(text)
        except ValueError:
            return False
        return {'number': number}
