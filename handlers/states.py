from aiogram.fsm.state import State, StatesGroup


class CreateTaskStates(StatesGroup):
    create_title = State()
    create_description = State()
    create_cancel_time = State()
    cancel_time_day = State()
    cancel_time_month = State()
    cancel_time_year = State()
    cancel_time_hour = State()
    cancel_time_minute = State()
