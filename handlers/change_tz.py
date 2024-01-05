from gettext import gettext as _

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from handlers.states import ChangePersonalConfig
from filters import CheckIntText
from storage.manage_storage import change_tz_user
from keyboards.kb_common_cmd import kb_inline_main_menu

router = Router()


@router.message(ChangePersonalConfig.change_timezone, F.text, CheckIntText())
@router.callback_query(ChangePersonalConfig.change_timezone, F.data, CheckIntText())
async def take_int_for_timezone_ok(query_message: types.CallbackQuery | types.Message, state: FSMContext, number: int) -> None:
    keyboard = await kb_inline_main_menu()
    text = _('Ваш часовой пояс был изменён')
    user_id: int = query_message.from_user.id
    await change_tz_user(user_id=user_id, new_tz=number)
    if isinstance(query_message, types.CallbackQuery):
        await query_message.message.edit_text(text=text, reply_markup=keyboard)
    else:  # isinstance(query_message, types.Message):
        await query_message.answer(text=text, reply_markup=keyboard)
    await state.clear()
