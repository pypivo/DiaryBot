from datetime import datetime
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from db.engine import async_session
from db.models.schedule import Schedule
from handlers.state.fms_schedule import FSMSchedule
from handlers.utils import create_days_markup, create_time_start_end, change_time_for_send

days = ['Понедельник', 'Вторник', "Среда", "Четверг",
        "Пятница", "Суббота", "Воскресенье"]

async def get_schedule(weekday: int = 0, message: Union[types.Message, types.CallbackQuery] = None,
                       day_of_week: str = None):
    user_id = str(message.from_user.id)
    if day_of_week is None: day_of_week = days[weekday].lower()

    if type(message) == types.CallbackQuery: send_message = message.message
    else: send_message = message

    if day_of_week[-1] == 'а':
        day_for_client = day_of_week[:-1] + 'y'
    else:
        day_for_client = day_of_week
    schedules = await Schedule.get_schedule(user_id, day_of_week, async_session)
    if not schedules:
        await send_message.answer(f'Расписание на {day_for_client} не заполнено.')
    else:
        await send_message.answer(f'Расписание на {day_for_client}:')
        for i, s in enumerate(schedules):
            s: Schedule
            time = change_time_for_send(s.time_start, s.time_end)
            await send_message.answer(f'{i + 1}). {s.name} с {time[0]} до {time[1]}.\n'
                                 f'Описание:\n{s.description}')
    return schedules

async def send_schedule_today(message: types.Message):
    weekday = datetime.today().weekday()
    await get_schedule(weekday, message)

async def send_schedule_week(message: types.Message):
    for day in range(7):
        await get_schedule(weekday=day, message=message)

async def schedule_start(message: types.Message):
    markup = create_days_markup()
    await FSMSchedule.day_of_week.set()
    await message.answer('Выберите день недели:', reply_markup=markup)

async def schedule_day(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['day_of_week'] = call.data.lower()
    await FSMSchedule.next()
    async with state.proxy() as data:
        data['user_id'] = str(call.from_user.id)
    await FSMSchedule.next()
    await call.message.answer(f'Готов добавить твое расписание на {call.data.lower()}!\n'
                      'Если отправил что-то не то, напиши стоп')
    await call.message.answer('Пришли время, на которое хочешь записать🕐\n\n'
                      'Пример:\n'
                      '16:00-17:00')

async def schedule_time(message: types.Message, state: FSMContext):
    # написать проверку на корректность времени
    time = create_time_start_end(message.text)
    if time:
        async with state.proxy() as data:
            data['time_start'] = time[0]
        await FSMSchedule.next()
        async with state.proxy() as data:
            data['time_end'] = time[1]
        await FSMSchedule.next()
        await message.reply("Введи название занятия")
    else:
        await message.reply('Некорректно введено время!\n'
                            'Введите ещё раз. Для отмены напишите стоп.')

async def schedule_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMSchedule.next()
    await message.reply("Введите описание занятия\n"
                        "Если не нужно, напишите стоп")

async def schedule_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await state.finish()
    await Schedule.create_schedule(data, session=async_session)
    await message.reply("Отлично, занятие записано")

# Выход из состояния
async def cansel_schedule(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ок')

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_schedule_today, commands='today')
    dp.register_message_handler(send_schedule_week, commands='week')
    dp.register_message_handler(schedule_start, commands='schedule', state=None)
    dp.register_message_handler(cansel_schedule, state='*', commands='стоп')
    dp.register_message_handler(cansel_schedule, Text(equals='стоп', ignore_case=True), state='*')
    dp.register_callback_query_handler(schedule_day, state=FSMSchedule.day_of_week)
    dp.register_message_handler(schedule_time, state=FSMSchedule.time_start)
    dp.register_message_handler(schedule_name, state=FSMSchedule.name)
    dp.register_message_handler(schedule_description, state=FSMSchedule.description)


