from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMSchedule(StatesGroup):
    day_of_week = State()
    time = State()
    name = State()
    description = State()