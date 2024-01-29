import re
from datetime import datetime

from aiogram.filters import BaseFilter
from aiogram.types import Message


class HasDateTimeFilter(BaseFilter):

    @staticmethod
    async def check_datetime(text) -> bool | datetime:
        pattern = r'\d\d.\d\d.\d\d\d\d\s\d\d:\d\d'
        find: re.Match | None = re.search(pattern=pattern, string=text)
        if find:
            date_string: str = find.group()
            return datetime.strptime(date_string, '%d.%m.%Y %H:%M')
        return False

    async def __call__(self, message: Message) -> bool | dict:
        # message.text: str
        find_datetime: datetime | bool = await self.check_datetime(text=message.text)
        if find_datetime:
            return {'cancel_time': find_datetime}
        return False


def correct_day(day: int, month: int, year: int):
    leap_year = (not year % 4) or (not year % 100 and not year % 400)
    month_days_list = {
        1: 31,
        2: 29 if leap_year else 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }
    max_day = month_days_list[month]
    return day if day <= max_day else max_day
