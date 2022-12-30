from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMSchedule(StatesGroup):
    day_of_week = State()
    user_id = State()
    time_start = State()
    time_end = State()
    name = State()
    description = State()

class FSMDeleteSchedule(StatesGroup):
    day_of_week = State()
    schedules = State()
    number_schedule = State()
    are_you_sure = State()