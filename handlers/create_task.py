from datetime import datetime

from aiogram import Router, F, types, filters
from aiogram.fsm.context import FSMContext

from handlers.states import CreateTaskStates
from filters import HasDateTimeFilter
from storage.manage_storage import add_task


router = Router()


# Шаг 1-ый - успех
@router.message(CreateTaskStates.create_title, F.text, F.text.len() <= 30)
async def create_task_title_ok(message: types.Message, state: FSMContext) -> None:
    title: str = message.text
    await state.update_data(title=title)
    await state.set_state(state=CreateTaskStates.create_description)
    await message.answer(text=f'Я запомнил название задачи: {title}'
                              f'\nТеперь напишите описание (до 128-ти символов) или'
                              f'\n/skip чтобы оставить это поле пустым')


# Шаг 1-ый - ошибка
@router.message(CreateTaskStates.create_title, F.text, F.text.len() > 30)
async def create_task_title_long(message: types.Message) -> None:
    await message.answer(text='Слишком длинное название.'
                              '\nПопробуйте снова или'
                              '\n/cancel чтобы отменить сохранение')


# Шаг 2-ой - успех Или /skip
@router.message(CreateTaskStates.create_description, F.text, F.text.len() <= 128)
@router.message(CreateTaskStates.create_description, filters.Command('skip'))
async def create_task_description_ok(message: types.Message,
                                     state: FSMContext,
                                     command: filters.CommandObject | None = None) -> None:
    description: str | None = message.text if not command else None
    await state.update_data(description=description)
    await state.set_state(state=CreateTaskStates.create_cancel_time)
    # Необходимо подготовить клавиатуру, либо парсинг текста для извлечения даты и времени
    await message.answer(text='Отлично. Теперь необходимо назначит крайний срок')


# Шаг 2-ой - ошибка
@router.message(CreateTaskStates.create_description, F.text, F.text.len() > 128)
async def create_task_description_long(message: types.Message) -> None:
    await message.answer(text='Слишком длинное описание.'
                              '\nПопробуйте снова или'
                              '\n/cancel чтобы отменить сохранение')


# Шаг 3-ий - успех
@router.message(CreateTaskStates.create_cancel_time, F.text, HasDateTimeFilter())
async def create_task_cancel_time_ok(message: types.Message, cancel_time: datetime, state: FSMContext) -> None:
    cancel_task: datetime = cancel_time
    user_id: int = message.from_user.id
    data: dict = await state.get_data()
    add_task(user_id=user_id, title=data['title'], description=data['description'], cancel_task=cancel_task)
    await state.clear()
    await message.answer(text='Задача поставлена!')


# Шаг 3-ий - ошибка
@router.message(CreateTaskStates.create_cancel_time, F.text)
async def create_task_cancel_time_error(message: types.Message) -> None:
    await message.answer(text='Упс!'
                              '\nНе могу определить дату')


# Непредвиденная ситуация, например эмодзи, картинка и т.д.
@router.message(CreateTaskStates)
async def create_task_error(message: types.Message) -> None:
    await message.answer(text='Упс!'
                              '\nНичего не могу понять.'
                              '\nПопробуйте снова')
