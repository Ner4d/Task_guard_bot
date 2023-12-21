from aiogram import Router, F, types, filters
from aiogram.fsm.context import FSMContext

from handlers.states import CreateTaskStates


router = Router()


@router.message(filters.Command('start'))
async def cmd_start(message: types.Message) -> None:
    await message.answer(text='Я включён и готов к работе.'
                              '\nДля получения списка команд введите /help')


@router.message(filters.Command('help'))
async def cmd_help(message: types.Message) -> None:
    await message.answer(text='Список действующих команд:'
                              '\n/create - Создание задачи'
                              '\n/delete - Удаление задачи'
                              '\n/cancel - отменяет любое действие (сохранение, удаление и т.д.)')


@router.message(filters.Command('create'))
async def cmd_create(message: types.Message, state: FSMContext) -> None:
    await state.set_state(CreateTaskStates.create_title)
    await message.answer(text='Готов к созданию задачи.'
                              '\nНапишите название для задачи (до 30-ти символов)')


@router.message(filters.Command('cancel'))
async def cmd_cancel(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(text='Я всё отменил')
