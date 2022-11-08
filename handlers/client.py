from aiogram import types, Dispatcher


async def start_help(message: types.Message):
    await message.answer("Бот-органайзер📂\nДоступные команды:\n"
                         "1). Добавить постоянное расписание на день недели:  /schedule\n"
                         "2). Посмотреть сегодняшнее расписание: /today")

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_help, commands=['start', 'help'])



