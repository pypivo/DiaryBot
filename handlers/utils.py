from typing import Union

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from handlers.validation.time import check_correctness_time
from handlers.validation.errors import IncorrectTime

def change_time_for_send(time_start: str, time_end: str):
    time_1 = time_start[:2] + ":" + time_start[2:]
    time_2 = time_end[:2] + ":" + time_end[2:]
    return time_1, time_2


def create_time_start_end(time: str) -> Union[list, bool]:
    try:
        check_correctness_time(time)
        time = time.replace(" ", "").replace(":", "")
        time_list = time.split("-")
        return time_list
    except IncorrectTime:
        return False

def create_num_markup(num: int):
    markup = InlineKeyboardMarkup()
    for i in range(1, num+1):
        button = InlineKeyboardButton(str(i), callback_data=str(i))
        markup.add(button)
    return markup

def create_days_markup():
    days = ['Понедельник', 'Вторник', "Среда", "Четверг",
            "Пятница", "Суббота", "Воскресенье"]
    markup = InlineKeyboardMarkup()
    for day in days:
        button = InlineKeyboardButton(day, callback_data=day)
        markup.add(button)
    return markup

def create_sure_markup():
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton('Да', callback_data='Да')
    button_2 = InlineKeyboardButton('Нет', callback_data='Нет')
    markup.add(button_1)
    markup.add(button_2)
    return markup