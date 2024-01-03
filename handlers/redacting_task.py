from gettext import gettext as _
from datetime import datetime

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from static import B_TEXT, I_TEXT
from keyboards.kb_cancel_time import month_list, make_kb_result
from handlers.states import RedactingTaskStates


router = Router()


async def prepare_text_to_result(title: str, description: str | None, cancel_time: datetime) -> str:
    text_parts: list = [_('Название: {}').format(B_TEXT.format(title))]
    if description:
        text_parts.append(_('Описание: {}').format(I_TEXT.format(description)))
    word_month = month_list[cancel_time.month]
    format_datetime = cancel_time.strftime('%d {} %Y - %H:%M').format(word_month)
    text_parts.append(_('Крайний срок: {}').format(B_TEXT.format(format_datetime)))
    return '\n'.join(text_parts)


@router.message(RedactingTaskStates.redact_description, F.text, F.text.len() <= 128)
@router.message(RedactingTaskStates.redact_title, F.text, F.text.len() <= 30)
async def redact_title_ok(message: types.Message, state: FSMContext) -> None:
    keyboard = await make_kb_result()
    state_name = await state.get_state()
    if state_name == RedactingTaskStates.redact_title:
        await state.update_data(title=message.text)
    else:
        await state.update_data(description=message.text)
    data: dict = await state.get_data()
    text = await prepare_text_to_result(title=data['title'], description=data['description'], cancel_time=data['cancel_time'])
    await message.answer(text=text, reply_markup=keyboard, parse_mode='HTML')


@router.callback_query(F.data == 'redact_description')
async def button_redact_description(query: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(RedactingTaskStates.redact_description)
    await query.message.edit_text(text=_('Напишите описание (до 128-ти символов)'))
