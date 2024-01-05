from gettext import gettext as _

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from handlers.states import CreateTaskStates, RedactingTaskStates
from keyboards.kb_cancel_time import make_kb_change_default
from keyboards.kb_common_cmd import kb_inline_button_cancel, kb_inline_button_skip
from static import I_TEXT
from storage.manage_storage import get_user_tz

router = Router()


# Шаг 1-ый - успех
@router.message(CreateTaskStates.create_title, F.text, F.text.len() <= 30)
async def create_task_title_ok(message: types.Message, state: FSMContext) -> None:
    keyboard = await kb_inline_button_skip()
    title: str = message.text
    user_id: int = message.from_user.id
    user_tz: int = await get_user_tz(user_id=user_id)
    await state.update_data(title=title, user_tz=user_tz)
    await state.set_state(state=CreateTaskStates.create_description)
    await message.answer(
        text=_('Я запомнил название задачи: {}').format(title) + _('\nТеперь напишите описание (до 128-ти символов)'),
        reply_markup=keyboard
    )


# Шаг 1-ый - ошибка
@router.message(RedactingTaskStates.redact_title, F.text, F.text.len() > 30)
@router.message(CreateTaskStates.create_title, F.text, F.text.len() > 30)
async def create_task_title_long(message: types.Message) -> None:
    keyboard = await kb_inline_button_cancel()
    await message.answer(text=_('Слишком длинное название.'), reply_markup=keyboard)


# Шаг 2-ой - успех или skip
@router.callback_query(CreateTaskStates.create_description, F.data == 'skip')
@router.message(CreateTaskStates.create_description, F.text, F.text.len() <= 128)
async def create_task_description_ok(query_message: types.Message | types.CallbackQuery, state: FSMContext) -> None:
    keyboard: types.InlineKeyboardMarkup = await make_kb_change_default()
    await state.set_state(state=CreateTaskStates.create_cancel_time)
    text = _('Отлично. Теперь необходимо назначить крайний срок\n{}').format(
        I_TEXT.format(_("По умолчанию: завтра в это же время"))
    )
    if isinstance(query_message, types.Message):
        description = query_message.text
        await query_message.answer(text=text,
                                   reply_markup=keyboard,
                                   parse_mode='HTML')  # Далее следует логика в handlers.create_cancel_time
    else:  # query_message is types.CallbackQuery
        description = None
        await query_message.message.edit_text(text=text,
                                              reply_markup=keyboard,
                                              parse_mode='HTML')
    await state.update_data(description=description)


# Шаг 2-ой - ошибка
@router.message(RedactingTaskStates.redact_description, F.text, F.text.len() > 128)
@router.message(CreateTaskStates.create_description, F.text, F.text.len() > 128)
async def create_task_description_long(message: types.Message) -> None:
    keyboard = await kb_inline_button_skip()
    await message.answer(text=_('Слишком длинное описание.\nПопробуйте снова'), reply_markup=keyboard)


# Непредвиденная ситуация, например эмодзи, картинка и т.д.
@router.message(*CreateTaskStates)
async def create_task_error(message: types.Message) -> None:
    keyboard = await kb_inline_button_cancel()
    await message.answer(text=_('Упс!\nНичего не могу понять.\nПопробуйте снова'), reply_markup=keyboard)
