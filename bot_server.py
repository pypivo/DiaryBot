from aiogram.utils import executor

from create_bot import dp
from handlers import client
from handlers import schedule

client.register_handlers_client(dp)
schedule.register_handlers_client(dp)


executor.start_polling(dp, skip_updates=True)

