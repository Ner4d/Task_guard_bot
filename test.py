from datetime import datetime, time


some_date = datetime(day=31, month=12, year=2023)
print(some_date)
some_date += time(hour=18, minute=43)
print(some_date)

