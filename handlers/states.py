from aiogram.fsm.state import State, StatesGroup


class CreateTaskStates(StatesGroup):
    # create_start = State()
    create_title = State()
    create_description = State()
    create_cancel_time = State()
