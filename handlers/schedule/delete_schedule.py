from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from db.engine import async_session
from db.models.schedule import Schedule
from handlers.schedule.schedule import get_schedule
from handlers.state.fms_schedule import FSMDeleteSchedule
from handlers.utils import create_days_markup, create_time_start_end, change_time_for_send, \
    create_num_markup, create_sure_markup


async def del_schedule_start(message: types.Message):
    markup = create_days_markup()
    await FSMDeleteSchedule.day_of_week.set()
    await message.answer('Выберите день недели:', reply_markup=markup)

async def del_schedule_day(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['day_of_week'] = call.data.lower()
    await FSMDeleteSchedule.next()
    schedules = await get_schedule(day_of_week=call.data.lower(), message=call)
    async with state.proxy() as data:
        data['schedules'] = schedules
    await FSMDeleteSchedule.next()
    markup = create_num_markup(len(schedules))
    await call.message.answer('Выберите номер занятия:', reply_markup=markup)

async def del_schedule_num(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['number_schedule'] = call.data.lower()
    await FSMDeleteSchedule.next()
    markup = create_sure_markup()
    await call.message.answer('Вы уверены?', reply_markup=markup)

async def del_schedule_sure(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['are_you_sure'] = call.data.lower()
    if data['are_you_sure'] == 'да':
        schedule_id = data['schedules'][int(data['number_schedule']) - 1].id
        await Schedule.del_schedule_by_id(schedule_id=schedule_id, session=async_session)
        await call.message.reply('Занятие удалено')
    else:
        await call.message.reply('Ок')
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(del_schedule_start, commands='delete', state=None)
    dp.register_callback_query_handler(del_schedule_day, state=FSMDeleteSchedule.day_of_week)
    dp.register_callback_query_handler(del_schedule_num, state=FSMDeleteSchedule.number_schedule)
    dp.register_callback_query_handler(del_schedule_sure, state=FSMDeleteSchedule.are_you_sure)


