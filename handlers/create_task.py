from datetime import datetime

from aiogram import Router, F, types, filters
from aiogram.fsm.context import FSMContext

from handlers.states import CreateTaskStates
from keyboards.kb_cancel_time import make_kb_change_default
from static import I_TEXT


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
    keyboard: types.InlineKeyboardMarkup = await make_kb_change_default()
    await message.answer(text='Отлично. Теперь необходимо назначить крайний срок'
                              f'\n{I_TEXT.format("По умолчанию: завтра в это же время")}',
                         reply_markup=keyboard,
                         parse_mode='HTML')  # Далее следует логика в handlers.create_cancel_time


# Шаг 2-ой - ошибка
@router.message(CreateTaskStates.create_description, F.text, F.text.len() > 128)
async def create_task_description_long(message: types.Message) -> None:
    await message.answer(text='Слишком длинное описание.'
                              '\nПопробуйте снова или'
                              '\n/cancel чтобы отменить сохранение')


# Непредвиденная ситуация, например эмодзи, картинка и т.д.
@router.message(*CreateTaskStates)
async def create_task_error(message: types.Message) -> None:
    await message.answer(text='Упс!'
                              '\nНичего не могу понять.'
                              '\nПопробуйте снова')
