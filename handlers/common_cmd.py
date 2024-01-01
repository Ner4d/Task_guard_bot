import asyncio

from aiogram import Router, F, types, filters
from aiogram.fsm.context import FSMContext

from handlers.states import CreateTaskStates
from keyboards.kb_common_cmd import kb_main_menu, kb_back_in_menu


router = Router()


@router.message(filters.Command('start'))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    keyboard = await kb_main_menu()
    await state.clear()
    await message.answer(text='Я готов к работе. А вы?', reply_markup=keyboard)


@router.callback_query(F.data == 'main_menu')
async def button_back(query: types.CallbackQuery, state: FSMContext) -> None:
    keyboard = await kb_main_menu()
    await state.clear()
    await query.message.edit_text(text='Главное меню', reply_markup=keyboard)


@router.callback_query(F.data == 'help')
async def main_button_help(query: types.CallbackQuery) -> None:
    keyboard = await kb_back_in_menu()
    await query.message.edit_text(text='Вы можете использовать команду /cancel, чтобы сбросить всё', reply_markup=keyboard)


@router.callback_query(F.data == 'create_task')
async def main_button_create(query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    keyboard = await kb_back_in_menu()
    await state.set_state(CreateTaskStates.create_title)
    await query.message.edit_text(text='Введите название для задачи:', reply_markup=keyboard)
    await asyncio.sleep(5)
    await query.message.delete_reply_markup()


@router.callback_query(F.data == 'cancel')
@router.message(filters.Command('cancel'))
async def cmd_cancel(query_message: types.CallbackQuery | types.Message, state: FSMContext) -> None:
    keyboard = await kb_back_in_menu()
    await state.clear()
    if isinstance(query_message, types.Message):
        await query_message.answer(text='Я всё отменил', reply_markup=keyboard)
        await asyncio.sleep(5)
        await query_message.delete_reply_markup()
    else:
        await query_message.message.edit_text(text='Я всё отменил', reply_markup=keyboard)
        await asyncio.sleep(5)
        await query_message.message.delete_reply_markup()
