import asyncio

from aiogram import Bot
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy.engine import URL

from db import Base, async_engine, async_session, proceed_schemas
from handlers import client
from handlers.schedule import schedule, delete_schedule
from config import token, db_username, db_psw, db_port, db_host, db_name


storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)

client.register_handlers_client(dp)
schedule.register_handlers_client(dp)
delete_schedule.register_handlers_client(dp)

#proceed_schemas(async_engine, Base)

#await dp.start_polling(bot)

# asyncio.run(proceed_schemas(async_engine, Base))

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)