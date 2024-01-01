from aiogram import Router, F, types, filters
from aiogram.fsm.context import FSMContext

from handlers.states import CreateTaskStates, RedactingTaskStates
from keyboards.kb_common_cmd import kb_inline_main_menu, kb_inline_back_in_menu


router = Router()


@router.message(filters.Command('start'))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    keyboard = await kb_inline_main_menu()
    await state.clear()
    await message.answer(text='Я готов к работе. А вы?', reply_markup=keyboard)


@router.callback_query(F.data == 'main_menu')
async def button_back(query: types.CallbackQuery, state: FSMContext) -> None:
    keyboard = await kb_inline_main_menu()
    await state.clear()
    await query.message.edit_text(text='Главное меню', reply_markup=keyboard)


@router.callback_query(F.data == 'help')
async def main_button_help(query: types.CallbackQuery) -> None:
    keyboard = await kb_inline_back_in_menu()
    await query.message.edit_text(text='Вы можете использовать команду /cancel, чтобы сбросить всё и вернуться в главное меню',
                                  reply_markup=keyboard)


@router.callback_query(F.data == 'create_task')
@router.callback_query(F.data == 'redact_title')
async def main_button_create(query: types.CallbackQuery, state: FSMContext) -> None:
    keyboard = await kb_inline_back_in_menu()
    if query.data == 'create_task':
        await state.set_state(CreateTaskStates.create_title)
    else:
        await state.set_state(RedactingTaskStates.redact_title)
    await query.message.edit_text(text='Введите название для задачи:', reply_markup=keyboard)


@router.message(filters.Command('cancel'))
async def cmd_cancel(query_message: types.CallbackQuery | types.Message, state: FSMContext) -> None:
    keyboard = await kb_inline_main_menu()
    await state.clear()
    if isinstance(query_message, types.Message):
        await query_message.answer(text='Я всё отменил, вы снова в меню', reply_markup=keyboard)
    else:  # isinstance(query_message, types.CallbackQuery)
        await query_message.message.edit_text(text='Я всё отменил, вы снова в меню', reply_markup=keyboard)
