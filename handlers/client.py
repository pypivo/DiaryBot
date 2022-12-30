from aiogram import types, Dispatcher

from db.engine import async_session
from db.models.user import User

async def start_help(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    user = await User.create_user(user_id, username, async_session)

    await message.answer("Бот-органайзер📂\nДоступные команды:\n"
                         "1). Добавить расписание на день недели:  /schedule\n"
                         "2). Посмотреть сегодняшнее расписание: /today\n"
                         "3). Посмотреть на всю неделю: /week\n"
                         "4). Удалить запись в расписании: /delete")



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_help, commands=['start', 'help'])



