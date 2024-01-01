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


class RedactingTaskStates(StatesGroup):
    redact_title = State()
    redact_description = State()
    redact_date_day = State()
    redact_date_month = State()
    redact_date_year = State()
    redact_time_hour = State()
    redact_time_minute = State()
    redact_result = State()

