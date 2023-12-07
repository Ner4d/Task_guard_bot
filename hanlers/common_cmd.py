from aiogram import Router, F, types, filters


router = Router()


@router.message(filters.Command('start'))
async def cmd_start(message: types.Message) -> None:
    await message.answer(text='Я запущен и готов к работе.'
                              '\nДля получения списка команд введите /help')


@router.message(filters.Command('help'))
async def cmd_help(message: types.Message) -> None:
    await message.answer(text='Список действующих команд:'
                              '\n/create - Создание задачи'
                              '\n/delete - Удаление задачи')


@router.message(filters.Command('create'))
async def cmd_create(message: types.Message) -> None:
    await message.answer(text='Готов к созданию задачи')


@router.message(filters.Command('delete'))
async def cmd_delete(message: types.Message) -> None:
    await message.answer(text='Готов к удалению задачи')
