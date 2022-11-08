from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_days_markup():
    days = ['Понедельник', 'Вторник', "Среда", "Четверг",
            "Пятница", "Суббота", "Воскресенье"]
    markup = InlineKeyboardMarkup()
    for day in days:
        button = InlineKeyboardButton(day, callback_data=day)
        markup.add(button)
    return markup