from datetime import datetime
import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class HasDateTimeFilter(BaseFilter):

    @staticmethod
    async def check_datetime(text) -> bool | datetime:
        pattern = r'\d\d.\d\d.\d\d\d\d\s\d\d:\d\d'
        find: re.Match | None = re.search(pattern=pattern, string=text)
        if find:
            date_string: str = find.group()
            return datetime.strptime(__date_string=date_string, __format='%d.%m.%Y %H:%M')
        return False

    async def __call__(self, message: Message) -> bool | dict:
        # message.text: str
        find_datetime: datetime | bool = await self.check_datetime(text=message.text)
        if find_datetime:
            return {'cancel_time': find_datetime}
        return False
