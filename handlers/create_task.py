from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from handlers.states import CreateTaskStates, RedactingTaskStates
from keyboards.kb_cancel_time import make_kb_change_default
from keyboards.kb_common_cmd import kb_inline_button_cancel, kb_inline_button_skip
from static import I_TEXT

router = Router()


# Шаг 1-ый - успех
@router.message(CreateTaskStates.create_title, F.text, F.text.len() <= 30)
async def create_task_title_ok(message: types.Message, state: FSMContext) -> None:
    keyboard = await kb_inline_button_skip()
    title: str = message.text
    await state.update_data(title=title)
    await state.set_state(state=CreateTaskStates.create_description)
    await message.answer(text=f'Я запомнил название задачи: {title}'
                              f'\nТеперь напишите описание (до 128-ти символов)', reply_markup=keyboard)


# Шаг 1-ый - ошибка
@router.message(RedactingTaskStates.redact_title, F.text, F.text.len() > 30)
@router.message(CreateTaskStates.create_title, F.text, F.text.len() > 30)
async def create_task_title_long(message: types.Message) -> None:
    keyboard = await kb_inline_button_cancel()
    await message.answer(text='Слишком длинное название.', reply_markup=keyboard)


# Шаг 2-ой - успех или skip
@router.callback_query(CreateTaskStates.create_description, F.data == 'skip')
@router.message(CreateTaskStates.create_description, F.text, F.text.len() <= 128)
async def create_task_description_ok(query_message: types.Message | types.CallbackQuery, state: FSMContext) -> None:
    keyboard: types.InlineKeyboardMarkup = await make_kb_change_default()
    await state.set_state(state=CreateTaskStates.create_cancel_time)
    if isinstance(query_message, types.Message):
        description = query_message.text
        await query_message.answer(text='Отлично. Теперь необходимо назначить крайний срок'
                                        f'\n{I_TEXT.format("По умолчанию: завтра в это же время")}',
                                   reply_markup=keyboard,
                                   parse_mode='HTML')  # Далее следует логика в handlers.create_cancel_time
    else:  # query_message is types.CallbackQuery
        description = None
        await query_message.message.edit_text(text='Отлично. Теперь необходимо назначить крайний срок'
                                                   f'\n{I_TEXT.format("По умолчанию: завтра в это же время")}',
                                              reply_markup=keyboard,
                                              parse_mode='HTML')
    await state.update_data(description=description)


# Шаг 2-ой - ошибка
@router.message(RedactingTaskStates.redact_description, F.text, F.text.len() > 128)
@router.message(CreateTaskStates.create_description, F.text, F.text.len() > 128)
async def create_task_description_long(message: types.Message) -> None:
    keyboard = await kb_inline_button_skip()
    await message.answer(text='Слишком длинное описание.'
                              '\nПопробуйте снова', reply_markup=keyboard)


# Непредвиденная ситуация, например эмодзи, картинка и т.д.
@router.message(*CreateTaskStates)
async def create_task_error(message: types.Message) -> None:
    keyboard = await kb_inline_button_cancel()
    await message.answer(text='Упс!'
                              '\nНичего не могу понять.'
                              '\nПопробуйте снова', reply_markup=keyboard)
