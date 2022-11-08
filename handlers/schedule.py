from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from create_bot import dp, bot
from handlers.state.fms_schedule import FSMSchedule
from utils import create_days_markup

async def schedule_start(message: types.Message):
    markup = create_days_markup()
    await FSMSchedule.day_of_week.set()
    await message.answer('Выберите день недели:', reply_markup=markup)

async def schedule_day(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['day_of_week'] = call.data.lower()
    await FSMSchedule.next()
    await bot.send_message(call.from_user.id, f'Готов добавить твое расписание на {call.data.lower()}!\n'
                                              'Если отправил что-то не то, напиши стоп')
    await bot.send_message(call.from_user.id, 'Пришли время, на которое хочешь записать🕐\n\n'
                                              'Пример:\n'
                                              '16:00-17:00')

async def schedule_time(message: types.Message, state: FSMContext):
    # написать проверку на корректность времени
    async with state.proxy() as data:
        data['time'] = message.text
    await FSMSchedule.next()
    await message.reply("Введи название занятия")

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
    await message.reply("Отлично, занятие записано")

# Выход из состояния
async def cansel_schedule(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ок')

def register_handlers_client(dp: Dispatcher):
    days = ['Понедельник', 'Вторник', "Среда", "Четверг",
            "Пятница", "Суббота", "Воскресенье"]
    dp.register_message_handler(schedule_start, commands='schedule', state=None)
    dp.register_message_handler(cansel_schedule, state='*', commands='стоп')
    dp.register_message_handler(cansel_schedule, Text(equals='стоп', ignore_case=True), state='*')
    dp.register_callback_query_handler(schedule_day, lambda c: c.data in days, state=FSMSchedule.day_of_week)
    dp.register_message_handler(schedule_time, state=FSMSchedule.time)
    dp.register_message_handler(schedule_name, state=FSMSchedule.name)
    dp.register_message_handler(schedule_description, state=FSMSchedule.description)


