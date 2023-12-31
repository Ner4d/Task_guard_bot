from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class CheckIntText(BaseFilter):
    int_str = '1234567890'

    async def __call__(self, query: CallbackQuery) -> bool | dict:
        if query.data[0] in self.int_str:
            number = int(query.data)
            return {'number': number}
        return False
